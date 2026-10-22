"""
agents.tools.git_tool — Envoltorio sobre el binario `git`.

Se usa `git` por subprocess a propósito, no GitPython: es una dependencia
menos y cubre el 100% de lo que necesita `GitAgent` (diff, log, status).
"""

from __future__ import annotations

import re
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from agents.tools.process_tool import ProcessResult, run_command
from agents.tools.registry import register_tool

_CONVENTIONAL_COMMIT_RE = re.compile(
    r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(?P<scope>\([^)]+\))?(?P<breaking>!)?: (?P<subject>.+)$"
)

# Heurística de clasificación por ruta de archivo tocado -> tipo de Conventional Commit.
# No es infalible (un cambio en tests/ podría ser un "fix" real), pero da una
# sugerencia razonable de partida — el commit final lo revisa una persona.
_PATH_TYPE_HINTS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^tests?/"), "test"),
    (re.compile(r"^docs?/"), "docs"),
    (re.compile(r"README|CHANGELOG"), "docs"),
    (re.compile(r"^\.github/"), "ci"),
    (re.compile(r"Dockerfile|docker-compose"), "build"),
    (re.compile(r"pyproject\.toml|uv\.lock|requirements"), "build"),
]


@register_tool("git")
@dataclass
class GitTool:
    repo_root: Path

    def _git(self, *args: str, check: bool = False) -> ProcessResult:
        return run_command(["git", *args], cwd=self.repo_root, check=check)

    def is_repo(self) -> bool:
        return self._git("rev-parse", "--is-inside-work-tree").ok

    def checked(self, *args: str) -> str:
        """Git con error explícito; también propaga timeouts del process_tool."""
        return self._git(*args, check=True).stdout.rstrip("\r\n")

    def upstream(self) -> dict:
        branch = self.checked("symbolic-ref", "--quiet", "--short", "HEAD")
        remote = self.checked("config", "--get", f"branch.{branch}.remote")
        ref = self.checked("config", "--get", f"branch.{branch}.merge")
        if remote == "." or not ref.startswith("refs/heads/") or "\n" in ref:
            raise ValueError("Se requiere un upstream remoto único de rama.")
        upstream = self.checked("rev-parse", "--symbolic-full-name", "@{upstream}")
        fetch_urls = self.checked("remote", "get-url", "--all", remote).splitlines()
        push_urls = self.checked("remote", "get-url", "--push", "--all", remote).splitlines()
        if len(fetch_urls) != 1 or len(push_urls) != 1:
            raise ValueError("Se requiere una única URL de fetch y de push.")
        return {"branch": branch, "remote": remote, "ref": ref, "upstream": upstream,
                "fetch_urls": fetch_urls, "push_urls": push_urls,
                "fetch_url": fetch_urls[0], "push_url": push_urls[0]}

    def sync_upstream(self) -> dict:
        """Fetch + pull ff-only. Árbol sucio solo si no hay nada que integrar."""
        with self._exclusive():
            return self._sync_upstream()

    @contextmanager
    def _exclusive(self):
        # fetch/pull comparten FETCH_HEAD. Dos preflights simultáneos del
        # mismo clon no pueden intercalar sus comandos (ni con un publish).
        # Windows no tiene fcntl: allí el bloqueo lo da msvcrt.
        import os

        directory = Path(self.checked("rev-parse", "--git-common-dir"))
        if not directory.is_absolute():
            directory = self.repo_root / directory
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / "geas-sync.lock").open("a+") as lock:
            if os.name == "nt":
                import msvcrt

                try:
                    lock.seek(0)
                    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                except OSError as exc:
                    raise ValueError("Otra sincronización/publicación Git de este clon está en curso; repite.") from exc
                try:
                    yield
                finally:
                    try:
                        lock.seek(0)
                        msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
                    except OSError:
                        pass
            else:
                import fcntl

                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as exc:
                    raise ValueError("Otra sincronización/publicación Git de este clon está en curso; repite.") from exc
                try:
                    yield
                finally:
                    fcntl.flock(lock, fcntl.LOCK_UN)

    def _sync_upstream(self) -> dict:
        state = self.upstream()
        if state["fetch_urls"] != state["push_urls"]:
            raise ValueError("pushurl difiere del remoto de lectura; no se puede verificar la publicación.")
        if self.checked("ls-files", "--unmerged"):
            raise ValueError("Git tiene conflictos sin resolver.")
        for marker in ("MERGE_HEAD", "rebase-merge", "rebase-apply", "CHERRY_PICK_HEAD", "REVERT_HEAD"):
            path = Path(self.checked("rev-parse", "--git-path", marker))
            if not path.is_absolute():
                path = self.repo_root / path
            if path.exists():
                raise ValueError(f"Git tiene una operación pendiente: {marker}.")
        self.checked("fetch", "--", state["remote"])
        ahead, behind = map(int, self.checked(
            "rev-list", "--left-right", "--count", "HEAD...@{upstream}"
        ).split())
        if ahead and behind:
            raise ValueError("Git divergente: resuelve la divergencia antes de trabajar.")
        dirty = bool(self.checked("status", "--porcelain", "--untracked-files=all"))
        if behind and dirty:
            raise ValueError("Hay commits entrantes y árbol sucio; conserva/commitea tu trabajo antes del pull.")
        if not dirty:
            # `pull` vuelve a hacer fetch. Con árbol sucio no se llama para que
            # un commit llegado entre ambos fetch no se integre a escondidas.
            self.checked("-c", "rebase.autoStash=false", "-c", "merge.autoStash=false",
                         "pull", "--ff-only", "--no-rebase", "--no-autostash",
                         "--", state["remote"], state["ref"])
        final = self.upstream()
        if self._destination(final) != self._destination(state):
            raise ValueError("El destino Git cambió durante la sincronización.")
        return {**state, "head": self.checked("rev-parse", "HEAD"), "ahead": ahead}

    @staticmethod
    def _destination(state: dict) -> dict:
        return {key: state.get(key) for key in (
            "branch", "remote", "ref", "upstream", "fetch_urls", "push_urls",
        )}

    def publish(self, expected_head: str, expected_destination: dict | None = None) -> dict:
        """Publica exactamente el SHA probado y verifica el remoto por ls-remote."""
        with self._exclusive():
            return self._publish(expected_head, expected_destination)

    def _publish(self, expected_head: str, expected_destination: dict | None = None) -> dict:
        state = self.upstream()
        if state["fetch_urls"] != state["push_urls"]:
            raise ValueError("pushurl difiere del remoto de lectura; no se puede verificar la publicación.")
        if expected_destination and self._destination(state) != self._destination(expected_destination):
            raise ValueError("El destino Git cambió después de la puerta; repite el cierre.")
        if self.checked("rev-parse", "HEAD") != expected_head:
            raise ValueError("HEAD cambió después de la puerta; vuelve a verificar.")
        # Se publica contra la URL fijada, no contra el nombre del remoto: un
        # `remote set-url` concurrente no puede desviar el push.
        self.checked("push", "--porcelain", "--no-follow-tags", "--",
                     state["push_url"], f"{expected_head}:{state['ref']}")
        lines = self.checked("ls-remote", "--exit-code", "--refs",
                             state["push_url"], state["ref"]).splitlines()
        if lines != [f"{expected_head}\t{state['ref']}"]:
            raise ValueError("El SHA publicado no coincide con HEAD probado.")
        if self.checked("rev-parse", "HEAD") != expected_head:
            raise ValueError("HEAD cambió durante el push; vuelve a verificar.")
        final = self.upstream()
        if self._destination(final) != self._destination(state):
            raise ValueError("El destino Git cambió durante el push; repite el cierre.")
        return {**state, "published": expected_head}

    def status_porcelain(self) -> list[tuple[str, str]]:
        """Devuelve [(código_estado, ruta), ...] tal y como `git status --porcelain`."""
        result = self._git("status", "--porcelain")
        entries = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            code, path = line[:2].strip(), line[3:].strip()
            entries.append((code, path))
        return entries

    def diff(self, *, staged: bool = False, name_only: bool = False) -> str:
        args = ["diff"]
        if staged:
            args.append("--staged")
        if name_only:
            args.append("--name-only")
        return self._git(*args).stdout

    def diff_stat(self, *, staged: bool = False) -> str:
        args = ["diff", "--stat"]
        if staged:
            args.insert(1, "--staged")
        return self._git(*args).stdout

    def changed_files(self, *, staged: bool = False) -> list[str]:
        raw = self.diff(staged=staged, name_only=True)
        files = [f for f in raw.splitlines() if f.strip()]
        if not files and staged:
            # nada en staging: mirar también working tree, es lo que suele querer el usuario
            files = [f for f in self.diff(staged=False, name_only=True).splitlines() if f.strip()]
        return files

    def log(self, *, max_count: int = 20, since_tag: str | None = None) -> list[dict[str, str]]:
        """Devuelve una lista de commits como dicts {hash, subject, author, date}."""
        rev_range = f"{since_tag}..HEAD" if since_tag else "HEAD"
        fmt = "%H%x1f%s%x1f%an%x1f%ad"
        result = self._git(
            "log", rev_range, f"--max-count={max_count}", f"--pretty=format:{fmt}", "--date=short"
        )
        commits = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            parts = line.split("\x1f")
            if len(parts) == 4:
                commits.append(
                    {"hash": parts[0], "subject": parts[1], "author": parts[2], "date": parts[3]}
                )
        return commits

    def last_tag(self) -> str | None:
        result = self._git("describe", "--tags", "--abbrev=0")
        return result.stdout.strip() or None if result.ok else None

    def current_branch(self) -> str:
        return self._git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()

    def commit(self, message: str) -> ProcessResult:
        return self._git("commit", "-m", message)

    def add(self, *paths: str) -> ProcessResult:
        return self._git("add", *paths)

    def create_tag(self, tag: str, *, message: str | None = None) -> ProcessResult:
        if message:
            return self._git("tag", "-a", tag, "-m", message)
        return self._git("tag", tag)

    def tag_exists(self, tag: str) -> bool:
        return self._git("rev-parse", tag).ok

    @staticmethod
    def parse_conventional_commit(message: str) -> dict[str, str] | None:
        """Extrae {type, scope, breaking, subject} de un mensaje Conventional Commits, o None."""
        match = _CONVENTIONAL_COMMIT_RE.match(message.strip().splitlines()[0])
        if not match:
            return None
        data = match.groupdict()
        data["scope"] = (data["scope"] or "").strip("()")
        data["breaking"] = bool(data["breaking"])
        return data

    @staticmethod
    def guess_commit_type(changed_files: list[str]) -> str:
        """Heurística: infiere el tipo Conventional Commit dominante a partir de las rutas tocadas."""
        if not changed_files:
            return "chore"
        counts: dict[str, int] = {}
        for path in changed_files:
            matched = False
            for pattern, commit_type in _PATH_TYPE_HINTS:
                if pattern.search(path):
                    counts[commit_type] = counts.get(commit_type, 0) + 1
                    matched = True
                    break
            if not matched:
                counts["feat"] = counts.get("feat", 0) + 1
        return max(counts, key=counts.get)
