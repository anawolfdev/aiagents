"""API HTTP local + remotos bare: ningún test toca GEAS/origin reales."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from dataclasses import replace
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from agents.agents.git_agent import GitAgent
from agents.agents.harness_agent import HarnessAgent
from agents.cli import _parse_kwargs, main
from agents.config import ProjectConfig
from agents.context import SharedContext
from agents.geas_sync import synchronize
from agents.tools.geas_tool import GeasClient, GeasError
from agents.tools.git_tool import GitTool

ORG = "00000000-0000-4000-8000-000000000001"
REPO = "00000000-0000-4000-8000-000000000002"
ACTOR = "00000000-0000-4000-8000-000000000003"
OTHER = "00000000-0000-4000-8000-000000000004"
TICKET = "00000000-0000-4000-8000-000000000005"
ROOT = Path(__file__).resolve().parents[2]


def git(root, *args, check=True):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=check).stdout.strip()


def commit(root, message="test"):
    git(root, "add", "-A")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", message)
    return git(root, "rev-parse", "HEAD")


@pytest.fixture
def api(monkeypatch):
    monkeypatch.setenv("GEAS_ACTOR_ID", ACTOR)
    monkeypatch.delenv("HARNESS_ASSUME_YES", raising=False)
    monkeypatch.delenv("HARNESS_CONFIRM", raising=False)
    state = {
        "ticket": {"id": TICKET, "status": "FREE", "assigned_actor_id": None,
                   "commit_before": "", "commit_after": ""},
        "calls": [], "headers": [], "fail": {}, "claim": "normal", "complete": "normal",
        "context_id": REPO, "members": [TICKET], "repos": [REPO], "callback": None,
    }

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, body, code=200):
            self.send_response(code)
            self.end_headers()
            with suppress(BrokenPipeError, ConnectionResetError):
                self.wfile.write(body if isinstance(body, bytes) else json.dumps(body).encode())

        def do_GET(self):
            state["calls"].append("health")
            self.send({"status": "ok"})

        def do_POST(self):
            tool = self.path.removeprefix("/api/tools/")
            params = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            state["calls"].append(tool)
            state["headers"].append((self.headers["X-Geas-Actor"], self.headers["X-Geas-Organization"]))
            failure = state["fail"].get(tool)
            if failure:
                if failure == "timeout":
                    time.sleep(0.1)
                elif failure == "json":
                    self.send(b"{broken")
                    return
                elif failure == "shape":
                    self.send({"success": True, "data": []})
                    return
                else:
                    self.send({"success": False, "error": "FORBIDDEN"}, failure)
                    return
            if tool == "list_repositories":
                data = {"organization_id": ORG, "repositories": [{"id": r} for r in state["repos"]]}
            elif tool == "get_repository_context":
                data = {"id": state["context_id"], "tickets": [{"id": t} for t in state["members"]]}
            elif tool == "get_ticket":
                data = state["ticket"].copy()
            elif tool == "start_ticket":
                if state["callback"]:
                    state["callback"](tool)
                mode = state["claim"]
                if mode != "noop":
                    state["ticket"].update(status="IN_PROGRESS", commit_before=params["commit_before"],
                                           assigned_actor_id=OTHER if mode == "race" else ACTOR)
                if mode == "lost":
                    self.send({"error": "response lost"}, 500)
                    return
                data = {"id": TICKET, "status": "IN_PROGRESS"}  # MCP puede ignorar el fallo del CAS
            elif tool == "complete_ticket":
                if state["callback"]:
                    state["callback"](tool)
                mode = state["complete"]
                if mode != "noop":
                    state["ticket"].update(status="DONE", commit_after=params["commit_after"])
                    if mode == "race":
                        state["ticket"]["assigned_actor_id"] = OTHER
                if mode == "lost":
                    self.send({"error": "response lost"}, 500)
                    return
                data = {"status": "DONE"}
            elif tool == "block_ticket":
                state["ticket"]["status"] = "BLOCKED"
                data = {"status": "BLOCKED"}
            else:
                raise AssertionError(tool)
            self.send({"success": True, "data": data})

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.01), daemon=True)
    thread.start()
    state["url"] = f"http://127.0.0.1:{server.server_port}"
    yield state
    server.shutdown()
    server.server_close()
    thread.join()


@pytest.fixture
def remote(tmp_path, api):
    bare = tmp_path / "remote.git"
    git(tmp_path, "init", "--bare", "-q", str(bare))
    local = tmp_path / "local"
    git(tmp_path, "clone", "-q", str(bare), str(local))
    (local / ".gitignore").write_text("agents/workspace/\n__pycache__/\n.pytest_cache/\n")
    (local / ".geas.yml").write_text(
        f"mcp_url: {api['url']}\norganization_id: {ORG}\nrepository_id: {REPO}\n"
    )
    progress = local / "harness" / "progress"
    progress.mkdir(parents=True)
    (progress / "current.md").write_text("initial\n")
    (progress / "history.md").write_text("# History\n")
    (local / "harness" / "featureslist.json").write_text(json.dumps({"features": [{
        "id": "F-001", "title": "test", "description": "d", "acceptance_criteria": ["c"],
        "status": "pending", "depends_on": [], "geas_ticket_id": TICKET,
    }]}))
    (local / "init.sh").write_text('#!/bin/sh\nprintf \'{"ready":true,"checks":[]}\\n\'\n')
    commit(local)
    git(local, "push", "-u", "origin", "HEAD")
    peer = tmp_path / "peer"
    git(tmp_path, "clone", "-q", str(bare), str(peer))
    context = SharedContext(local, ProjectConfig())
    return HarnessAgent(context=context), local, peer, bare


def feature(local):
    return json.loads((local / "harness" / "featureslist.json").read_text())["features"][0]


def claim_and_commit(remote):
    harness, local, _, _ = remote
    assert harness.start(id="F-001").success
    (local / "product.py").write_text("value = 1\n")
    return commit(local)


def test_sync_pull_before_claim_and_readback(remote, api):
    harness, local, peer, _ = remote
    (peer / "incoming").write_text("upstream\n")
    incoming = commit(peer)
    git(peer, "push")
    api["callback"] = lambda _: (local / "incoming").is_file() or pytest.fail("claim before pull")
    result = harness.start(id="F-001")
    assert result.success, result
    assert api["ticket"]["commit_before"] == incoming
    assert feature(local)["status"] == "in_progress"
    assert api["calls"].index("get_repository_context") < api["calls"].index("start_ticket")
    assert api["calls"][-1] == "get_ticket"
    assert set(api["headers"]) == {(ACTOR, ORG)}


@pytest.mark.parametrize("mode,success", [("race", False), ("noop", False), ("lost", True)])
def test_claim_cas_readback_and_lost_response(remote, api, mode, success):
    harness, local, _, _ = remote
    api["claim"] = mode
    result = harness.start(id="F-001")
    assert result.success is success
    assert feature(local)["status"] == ("in_progress" if success else "pending")
    if success:
        current = local / "harness" / "progress" / "current.md"
        current.write_text(current.read_text() + "keep my log\n")
        assert harness.start(id="F-001").success
        assert current.read_text().endswith("keep my log\n")
    assert api["calls"].count("start_ticket") == 1


def test_link_reconciles_in_progress_without_reset(remote, api):
    harness, local, _, _ = remote
    assert harness.start(id="F-001").success
    docpath = local / "harness" / "featureslist.json"
    doc = json.loads(docpath.read_text())
    del doc["features"][0]["geas_ticket_id"]
    doc["features"][0]["review_rounds"] = 2
    docpath.write_text(json.dumps(doc))
    current = local / "harness" / "progress" / "current.md"
    current.write_text("keep progress\n")
    assert harness.link(id="F-001", ticket_id=TICKET).success
    assert feature(local)["review_rounds"] == 2
    assert current.read_text() == "keep progress\n"
    assert api["calls"].count("start_ticket") == 1


def test_explicit_mapping_repo_and_owner(remote, api):
    harness, local, _, _ = remote
    api["members"] = []
    assert not harness.start(id="F-001").success
    assert not harness.link(id="F-001", ticket_id=TICKET).success
    api["members"] = [TICKET]
    api["ticket"].update(status="IN_PROGRESS", assigned_actor_id=OTHER, commit_before=git(local, "rev-parse", "HEAD"))
    assert not harness.start(id="F-001").success
    assert not harness.record(id="F-001", agent="implementer", content="no").success
    assert not harness.block(id="F-001", reason="no").success
    assert "start_ticket" not in api["calls"]
    assert feature(local)["status"] == "pending"


def test_missing_and_duplicate_mapping(remote):
    harness, local, _, _ = remote
    path = local / "harness" / "featureslist.json"
    doc = json.loads(path.read_text())
    doc["features"].append({**doc["features"][0], "id": "F-002"})
    path.write_text(json.dumps(doc))
    assert not harness.start(id="F-001").success
    assert not harness.link(id="F-001", ticket_id=TICKET).success
    doc["features"] = doc["features"][:1]
    del doc["features"][0]["geas_ticket_id"]
    path.write_text(json.dumps(doc))
    assert not harness.start(id="F-001").success
    assert harness.start(id="F-001", ticket_id=TICKET).success


@pytest.mark.parametrize("action", ["status", "next", "sync", "start", "finish", "block", "add", "record", "link"])
def test_all_operations_fail_closed_without_actor(remote, monkeypatch, action, api):
    harness, local, _, _ = remote
    before = (local / "harness" / "featureslist.json").read_bytes()
    monkeypatch.delenv("GEAS_ACTOR_ID")
    monkeypatch.delenv("GEAS_ACTOR", raising=False)
    result = getattr(harness, action)()
    assert not result.success
    assert result.data["code"] == "ACTOR_REQUIRED"
    assert (local / "harness" / "featureslist.json").read_bytes() == before
    assert not api["calls"]


@pytest.mark.parametrize("failure", [401, 403, 500, "json", "shape"])
def test_http_failure_never_claims(remote, api, failure):
    harness, local, _, _ = remote
    api["fail"]["list_repositories"] = failure
    result = harness.start(id="F-001")
    assert not result.success
    assert feature(local)["status"] == "pending"
    assert "start_ticket" not in api["calls"]


def test_timeout_and_connection_failure(remote, api):
    _, local, _, _ = remote
    client = replace(GeasClient.from_root(local), timeout=0.01)
    api["fail"]["get_ticket"] = "timeout"
    with pytest.raises(GeasError, match="timeout"):
        client.ticket(TICKET)
    with pytest.raises(GeasError):
        replace(client, url="http://127.0.0.1:1").context()


@pytest.mark.parametrize("text", ["mcp_url: []", "mcp_url: http://user:pw@host", "bad yaml", "mcp_url: 'oops", "mcp_url: x\nmcp_url: y"])
def test_bad_config_blocks(remote, text):
    harness, local, _, _ = remote
    (local / ".geas.yml").write_text(text)
    assert not harness.sync().success


def test_actor_alias_and_wrong_repository(remote, api, monkeypatch):
    harness, _, _, _ = remote
    monkeypatch.delenv("GEAS_ACTOR_ID")
    monkeypatch.setenv("GEAS_ACTOR", ACTOR)
    assert harness.sync().success
    api["repos"] = [OTHER]
    assert not harness.sync().success


def test_dirty_current_allowed_dirty_behind_blocks(remote, api):
    harness, local, peer, _ = remote
    current = local / "harness" / "progress" / "current.md"
    current.write_text("user work\n")
    assert harness.sync().success
    (peer / "incoming").write_text("new\n")
    commit(peer)
    git(peer, "push")
    before = git(local, "rev-parse", "HEAD")
    result = harness.start(id="F-001")
    assert not result.success
    assert git(local, "rev-parse", "HEAD") == before
    assert current.read_text() == "user work\n"
    assert "start_ticket" not in api["calls"]


@pytest.mark.parametrize("problem", ["diverged", "upstream", "detached", "conflict", "merge", "fetch"])
def test_git_blockers_prevent_claim(remote, api, problem):
    harness, local, peer, _ = remote
    if problem == "diverged":
        (local / "local").write_text("local\n")
        commit(local)
        (peer / "incoming").write_text("incoming\n")
        commit(peer)
        git(peer, "push")
    elif problem == "upstream":
        git(local, "branch", "--unset-upstream")
    elif problem == "detached":
        git(local, "checkout", "--detach")
    elif problem == "conflict":
        # Real unmerged index: two branches change the same tracked file.
        git(local, "checkout", "-b", "other")
        (local / ".gitignore").write_text("other\n")
        commit(local)
        git(local, "checkout", "-")
        (local / ".gitignore").write_text("local\n")
        commit(local)
        git(local, "-c", "user.name=Test", "-c", "user.email=test@example.com", "merge", "other", check=False)
        assert git(local, "ls-files", "--unmerged")
    elif problem == "merge":
        (local / ".git" / "MERGE_HEAD").write_text(git(local, "rev-parse", "HEAD"))
    else:
        git(local, "remote", "set-url", "origin", str(local / "missing.git"))
    assert not harness.start(id="F-001").success
    assert "start_ticket" not in api["calls"]
    assert feature(local)["status"] == "pending"


def test_successful_close_checks_publication_before_done(remote, api):
    harness, local, _, bare = remote
    head = claim_and_commit(remote)
    before = git(local, "rev-list", "--count", "HEAD")

    def callback(tool):
        assert tool == "complete_ticket"
        assert git(bare, "rev-parse", "HEAD") == head
        assert feature(local)["status"] == "in_progress"

    api["callback"] = callback
    result = harness.run("finish", id="F-001", evidence="5 passed", confirm=True)
    assert result.success, result
    assert feature(local)["status"] == "done"
    assert feature(local)["geas_commit_after"] == head
    assert api["ticket"]["status"] == "DONE"
    assert git(local, "rev-list", "--count", "HEAD") == before  # no auto-commit
    assert "harness/featureslist.json" in git(local, "status", "--porcelain")
    assert "5 passed" in (local / "harness" / "progress" / "history.md").read_text()


def test_publish_does_not_follow_tags_or_push_to_multiple_urls(remote):
    harness, local, _, bare = remote
    head = claim_and_commit(remote)
    git(local, "config", "push.followTags", "true")
    git(local, "-c", "user.name=Test", "-c", "user.email=test@example.com", "tag", "-a", "test-tag", "-m", "tag")
    assert GitAgent(context=harness.ctx).run("publish", expected_head=head, confirm=True).success
    assert not git(bare, "tag", "--list")
    git(local, "config", "--add", "remote.origin.pushurl", str(bare))
    git(local, "config", "--add", "remote.origin.pushurl", str(local / "unexpected.git"))
    assert not GitAgent(context=harness.ctx).run("publish", expected_head=head, confirm=True).success


@pytest.mark.parametrize("confirm", [False, "false", "true", 1])
def test_close_without_boolean_confirmation_never_pushes(remote, api, confirm):
    harness, local, _, bare = remote
    old = git(bare, "rev-parse", "HEAD")
    claim_and_commit(remote)
    result = harness.run("finish", id="F-001", evidence="passed", confirm=confirm)
    assert not result.success
    assert result.needs
    assert git(bare, "rev-parse", "HEAD") == old
    assert "complete_ticket" not in api["calls"]
    assert feature(local)["status"] == "in_progress"


@pytest.mark.parametrize("problem", ["dirty", "evidence", "gate", "head", "owner", "push", "sync", "upstream", "pushurl"])
def test_close_blockers_never_mark_done(remote, api, problem, monkeypatch):
    harness, local, peer, bare = remote
    head = claim_and_commit(remote)
    if problem == "dirty":
        (local / "product.py").write_text("uncommitted\n")
    elif problem == "gate":
        (local / "init.sh").write_text('printf \'{"ready":false,"checks":[]}\\n\'; exit 1\n')
        commit(local)
    elif problem == "head":
        def changed_gate(**kwargs):
            (local / "changed_during_gate").write_text("changed\n")
            commit(local)
            return original_gate(**kwargs)
        original_gate = harness.gate
        monkeypatch.setattr(harness, "gate", changed_gate)
    elif problem == "owner":
        api["ticket"]["assigned_actor_id"] = OTHER
    elif problem == "push":
        hook = bare / "hooks" / "pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
    elif problem == "sync":
        def incoming_gate(**kwargs):
            (peer / "upstream").write_text("incoming\n")
            commit(peer)
            git(peer, "push")
            return original_gate(**kwargs)
        original_gate = harness.gate
        monkeypatch.setattr(harness, "gate", incoming_gate)
    elif problem == "upstream":
        git(local, "branch", "--unset-upstream")
    elif problem == "pushurl":
        git(local, "remote", "set-url", "--push", "origin", str(peer))
    result = harness.finish(id="F-001", evidence="" if problem == "evidence" else "passed", confirm=True)
    assert not result.success, (problem, head)
    assert feature(local)["status"] == "in_progress"
    assert "complete_ticket" not in api["calls"]


@pytest.mark.parametrize("mode,success", [("noop", False), ("race", False), ("lost", True)])
def test_complete_requires_readback(remote, api, mode, success):
    harness, local, _, _ = remote
    claim_and_commit(remote)
    api["complete"] = mode
    result = harness.finish(id="F-001", evidence="passed", confirm=True)
    assert result.success is success
    assert feature(local)["status"] == ("done" if success else "in_progress")


def test_remote_done_local_failure_retry_does_not_duplicate_history(remote, api, monkeypatch):
    harness, local, _, _ = remote
    claim_and_commit(remote)
    save = harness._save
    monkeypatch.setattr(harness, "_save", lambda _: (_ for _ in ()).throw(OSError("disk failure")))
    result = harness.finish(id="F-001", evidence="passed", confirm=True)
    assert not result.success
    assert api["ticket"]["status"] == "DONE"
    assert feature(local)["status"] == "in_progress"
    monkeypatch.setattr(harness, "_save", save)
    assert harness.finish(id="F-001", evidence="passed", confirm=True).success
    assert harness.finish(id="F-001", evidence="passed", confirm=True).success
    assert api["calls"].count("complete_ticket") == 1
    assert (local / "harness" / "progress" / "history.md").read_text().count("## F-001") == 1


def test_remote_done_wrong_sha_or_dirty_product_does_not_reconcile(remote, api):
    harness, local, _, _ = remote
    head = claim_and_commit(remote)
    api["ticket"].update(status="DONE", commit_after="a" * 40)
    assert not harness.finish(id="F-001", evidence="passed", confirm=True).success
    api["ticket"]["commit_after"] = head
    (local / "product.py").write_text("pending work\n")
    assert not harness.finish(id="F-001", evidence="passed", confirm=True).success
    assert feature(local)["status"] == "in_progress"


def test_claim_local_write_failure_can_be_retried_without_second_claim(remote, api, monkeypatch):
    harness, local, _, _ = remote
    save = harness._save
    monkeypatch.setattr(harness, "_save", lambda _: (_ for _ in ()).throw(OSError("disk failure")))
    assert not harness.start(id="F-001").success
    assert feature(local)["status"] == "pending"
    assert api["ticket"]["status"] == "IN_PROGRESS"
    monkeypatch.setattr(harness, "_save", save)
    assert harness.start(id="F-001").success
    assert api["calls"].count("start_ticket") == 1


def test_complete_readback_unavailable_then_reconciles(remote, api):
    harness, local, _, _ = remote
    claim_and_commit(remote)
    api["callback"] = lambda _: api["fail"].update(get_ticket=503)
    assert not harness.finish(id="F-001", evidence="passed", confirm=True).success
    assert feature(local)["status"] == "in_progress"
    assert api["ticket"]["status"] == "DONE"
    api["fail"].clear()
    assert harness.finish(id="F-001", evidence="passed", confirm=True).success
    assert api["calls"].count("complete_ticket") == 1


def test_remote_done_history_write_failure_is_atomic_and_recoverable(remote, api, monkeypatch):
    harness, local, _, _ = remote
    claim_and_commit(remote)
    original = Path.write_text

    def fail_write(path, text, *args, **kwargs):
        if path.name == "history.md.tmp":
            original(path, text[:40], *args, **kwargs)
            raise OSError("partial disk write")
        return original(path, text, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_write)
    assert not harness.finish(id="F-001", evidence="passed", confirm=True).success
    assert (local / "harness" / "progress" / "history.md").read_text() == "# History\n"
    assert not (local / "harness" / "progress" / "history.md.tmp").exists()
    monkeypatch.setattr(Path, "write_text", original)
    assert harness.finish(id="F-001", evidence="passed", confirm=True).success
    assert api["calls"].count("complete_ticket") == 1


@pytest.mark.parametrize("operation", ["fetch", "pull"])
def test_sync_git_timeouts_never_claim(remote, api, monkeypatch, operation):
    from agents.exceptions import ToolExecutionError
    harness, local, _, _ = remote
    checked = GitTool.checked

    def timeout(self, *args):
        if operation in args:
            raise ToolExecutionError(f"{operation} timeout")
        return checked(self, *args)

    monkeypatch.setattr(GitTool, "checked", timeout)
    assert not harness.start(id="F-001").success
    assert "start_ticket" not in api["calls"]
    assert feature(local)["status"] == "pending"


def test_concurrent_sync_is_blocked_before_interleaving_fetch_head(remote, api, monkeypatch):
    harness, local, _, _ = remote
    entered = threading.Event()
    release = threading.Event()
    checked = GitTool.checked

    def delayed_fetch(self, *args):
        if args[0] == "fetch":
            entered.set()
            assert release.wait(timeout=5)
        return checked(self, *args)

    monkeypatch.setattr(GitTool, "checked", delayed_fetch)
    before = git(local, "rev-parse", "HEAD")
    with ThreadPoolExecutor(max_workers=1) as pool:
        first = pool.submit(GitTool(local).sync_upstream)
        assert entered.wait(timeout=5)
        try:
            second = harness.start(id="F-001")
            assert not second.success
            assert "está en curso" in second.message
            assert "start_ticket" not in api["calls"]
        finally:
            release.set()
        assert first.result(timeout=5)["head"] == before
    assert harness.start(id="F-001").success  # lock released without stale state
    assert api["calls"].count("start_ticket") == 1


def test_config_changed_by_pull_requires_resync_before_claim(remote, api):
    harness, local, peer, _ = remote
    config = peer / ".geas.yml"
    config.write_text(config.read_text().replace(REPO, OTHER))
    commit(peer)
    git(peer, "push")
    result = harness.start(id="F-001")
    assert not result.success
    assert result.data["code"] == "CONFIG_CHANGED"
    assert "start_ticket" not in api["calls"]
    assert feature(local)["status"] == "pending"


def test_gate_pull_changing_head_cannot_publish_untested_sha(remote, api, monkeypatch):
    harness, local, peer, bare = remote
    assert harness.start(id="F-001").success
    commit(local)
    git(local, "push")
    git(peer, "pull", "--ff-only")
    tested = git(local, "rev-parse", "HEAD")
    gate = harness.gate

    def incoming_gate(**kwargs):
        (peer / "incoming.py").write_text("value = 2\n")
        commit(peer)
        git(peer, "push")
        return gate(**kwargs)

    monkeypatch.setattr(harness, "gate", incoming_gate)
    result = harness.finish(id="F-001", evidence="passed", confirm=True)
    assert not result.success
    assert result.data["code"] == "HEAD_CHANGED"
    assert git(local, "rev-parse", "HEAD") != tested
    assert git(local, "rev-parse", "HEAD") == git(bare, "rev-parse", "HEAD")
    assert "complete_ticket" not in api["calls"]


def test_push_timeout_or_wrong_publication_blocks_done(remote, api, monkeypatch):
    from agents.exceptions import ToolExecutionError
    harness, local, _, _ = remote
    claim_and_commit(remote)
    original = GitTool.checked

    def checked(self, *args):
        if args[0] == "push":
            raise ToolExecutionError("push timeout")
        return original(self, *args)

    monkeypatch.setattr(GitTool, "checked", checked)
    assert not harness.finish(id="F-001", evidence="passed", confirm=True).success
    assert "complete_ticket" not in api["calls"]
    assert feature(local)["status"] == "in_progress"

    def wrong_sha(self, *args):
        if args[0] == "ls-remote":
            return "a" * 40 + "\trefs/heads/master"
        return original(self, *args)

    monkeypatch.setattr(GitTool, "checked", wrong_sha)
    assert not harness.finish(id="F-001", evidence="passed", confirm=True).success
    assert "complete_ticket" not in api["calls"]


@pytest.mark.parametrize("flags,success", [(["--yes"], True), (["--confirm", "false"], False)])
def test_cli_publish_confirmation(remote, monkeypatch, capsys, flags, success):
    _, local, _, _ = remote
    head = claim_and_commit(remote)
    import agents.cli
    monkeypatch.setattr(agents.cli, "get_context", lambda: SharedContext(local, ProjectConfig()))
    code = main(["--json", "run", "git", "publish", "--expected-head", head, *flags])
    payload = json.loads(capsys.readouterr().out)
    assert payload["success"] is success
    assert code == (0 if success else 1)


def test_confirmation_only_forwarded_to_explicit_parameter(remote, monkeypatch):
    harness, local, _, _ = remote
    seen = {}

    def method(*, confirm=False, **kwargs):
        from agents.core.base_agent import AgentResult
        seen.update(confirm=confirm, **kwargs)
        return AgentResult(True, "harness", "finish", "ok")

    monkeypatch.setattr(harness, "actions", lambda: {"finish": method})
    assert harness.run("finish", **_parse_kwargs(["--yes"])).success
    assert seen["confirm"] is True
    assert harness.run("finish", **_parse_kwargs(["--confirm", "false"])).success
    assert seen["confirm"] is False
    assert not GitAgent(context=harness.ctx).run("publish", expected_head=git(local, "rev-parse", "HEAD"), confirm="false").success


def test_no_geas_preserves_local_mode(tmp_path, monkeypatch):
    monkeypatch.delenv("GEAS_ACTOR_ID", raising=False)
    assert synchronize(tmp_path).client is None  # no Git/network required in templates


def scaffold_init(local, tmp_path):
    shutil.copyfile(ROOT / "init.sh", local / "init.sh")
    (local / "AGENTS.md").write_text("test\n")
    definitions = local / ".opencode" / "agents"
    definitions.mkdir(parents=True)
    for name in ("lider", "implementer", "reviewer", "explorer"):
        (definitions / f"{name}.md").write_text("test\n")
    (local / "app").mkdir()
    (local / "project.yml").write_text("project_slug: app\n")
    (local / "pyproject.toml").write_text("[tool.pytest.ini_options]\n")
    (local / "tests").mkdir()
    (local / "tests" / "test_ok.py").write_text("def test_ok(): assert True\n")
    (local / "agents" / "tests").mkdir(parents=True)
    # Stub uv delegates to the real pytest interpreter without installing into
    # the disposable fixture. agents/tests fails so full init must detect it.
    (local / "agents" / "tests" / "test_regression.py").write_text("def test_agent_regression(): assert False\n")
    binaries = tmp_path / "bin"
    binaries.mkdir()
    uv = binaries / "uv"
    uv.write_text(f'#!/bin/sh\nif [ "$1" = "--version" ]; then printf "uv test\\n"; exit 0; fi\nshift\nexec "{sys.executable}" -m "$@"\n')
    uv.chmod(0o755)
    return {**os.environ, "PYTHONPATH": str(ROOT), "PATH": f"{binaries}:{os.environ['PATH']}"}


def test_init_json_quick_sync_and_full_agents_regressions(remote, api, tmp_path):
    _, local, _, _ = remote
    env = scaffold_init(local, tmp_path)
    quick = subprocess.run(["bash", "init.sh", "--quick", "--json"], cwd=local, env=env, capture_output=True, text=True, timeout=30)
    assert quick.returncode == 0, quick.stdout + quick.stderr
    assert json.loads(quick.stdout)["checks"][0]["check"] == "sync"
    assert api["calls"].count("health") == 2  # leaf sync, no recursion
    full = subprocess.run(["bash", "init.sh", "--json"], cwd=local, env=env, capture_output=True, text=True, timeout=30)
    assert full.returncode == 1, full.stdout + full.stderr
    assert any(c["check"] == "pytest" and c["status"] == "fail" for c in json.loads(full.stdout)["checks"])
    env.pop("GEAS_ACTOR_ID", None)
    env.pop("GEAS_ACTOR", None)
    blocked = subprocess.run(["bash", "init.sh", "--quick", "--json"], cwd=local, env=env, capture_output=True, text=True, timeout=30)
    report = json.loads(blocked.stdout)
    assert blocked.returncode == 1
    assert report["ready"] is False
    assert len(report["checks"]) == 1
    assert "ACTOR_REQUIRED" in report["checks"][0]["detail"]
    (local / ".geas.yml").unlink()
    offline = subprocess.run(["bash", "init.sh", "--quick", "--json"], cwd=local, env=env, capture_output=True, text=True, timeout=30)
    assert offline.returncode == 0, offline.stdout + offline.stderr


def test_concurrent_backlog_writes_never_lose_acknowledged_feature(remote, monkeypatch):
    first, local, _, _ = remote
    second = HarnessAgent(context=first.ctx)
    loaded = threading.Event()
    release = threading.Event()
    original_load = first._load

    def paused_load():
        doc = original_load()
        loaded.set()
        assert release.wait(10)
        return doc

    monkeypatch.setattr(first, "_load", paused_load)
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(first.add, id="FIRST", title="first", criteria="c")
        assert loaded.wait(10)
        try:
            rejected = second.add(id="SECOND", title="second", criteria="c")
        finally:
            release.set()
        assert pending.result(10).success
    ids = [f["id"] for f in json.loads((local / "harness" / "featureslist.json").read_text())["features"]]
    assert "FIRST" in ids
    if rejected.success:
        assert "SECOND" in ids


def test_claim_retry_preserves_progress_after_partial_local_write(remote, api, monkeypatch):
    harness, local, _, _ = remote
    original_save = harness._save
    monkeypatch.setattr(harness, "_save", lambda _: (_ for _ in ()).throw(OSError("disk failure")))
    assert not harness.start(id="F-001").success
    current = local / "harness" / "progress" / "current.md"
    current.write_text(current.read_text() + "\nVALUABLE RECOVERY NOTES\n")
    monkeypatch.setattr(harness, "_save", original_save)
    assert harness.start(id="F-001").success
    assert "VALUABLE RECOVERY NOTES" in current.read_text()
    assert api["calls"].count("start_ticket") == 1


def test_dirty_tree_never_pulls_commits_arriving_after_fetch(remote, api, monkeypatch):
    harness, local, peer, _ = remote
    (local / "local-notes.txt").write_text("uncommitted user work\n")
    original = GitTool.checked
    pulled = []

    def checked(self, *args):
        if args[0] == "pull":
            pulled.append(args)
            (peer / "incoming.txt").write_text("new upstream commit\n")
            commit(peer)
            git(peer, "push")
        return original(self, *args)

    monkeypatch.setattr(GitTool, "checked", checked)
    before = git(local, "rev-parse", "HEAD")
    assert harness.start(id="F-001").success
    assert not pulled
    assert git(local, "rev-parse", "HEAD") == before
    assert (local / "local-notes.txt").read_text() == "uncommitted user work\n"


def test_gate_cannot_redirect_push_to_new_destination(remote, api, monkeypatch, tmp_path):
    harness, local, _, bare = remote
    head = claim_and_commit(remote)
    other = tmp_path / "other.git"
    git(tmp_path, "clone", "--bare", "-q", str(bare), str(other))
    original_bare_head = git(bare, "rev-parse", "HEAD")
    gate = harness.gate

    def changing_gate(**kwargs):
        result = gate(**kwargs)
        git(local, "remote", "set-url", "origin", str(other))
        return result

    monkeypatch.setattr(harness, "gate", changing_gate)
    result = harness.finish(id="F-001", evidence="passed", confirm=True)
    assert not result.success
    assert git(bare, "rev-parse", "HEAD") == original_bare_head
    assert git(other, "rev-parse", "HEAD") == original_bare_head
    assert head != git(other, "rev-parse", "HEAD")
    assert "complete_ticket" not in api["calls"]
    assert feature(local)["status"] == "in_progress"


def test_shell_wrappers_are_syntactically_valid():
    for name in ("init.sh", "sync.sh", "start.sh", "finish.sh", "status.sh"):
        result = subprocess.run(["bash", "-n", str(ROOT / name)], capture_output=True, text=True)
        assert result.returncode == 0, (name, result.stderr)
