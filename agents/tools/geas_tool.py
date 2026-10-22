"""Cliente HTTP stdlib de GEAS. Nunca abre el almacenamiento del servidor."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from uuid import UUID


class GeasError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class GeasClient:
    url: str
    organization_id: str
    repository_id: str
    actor_id: str
    timeout: float = 10

    @classmethod
    def from_root(cls, root: Path) -> GeasClient | None:
        path = root / ".geas.yml"
        if not path.exists():
            return None
        # Este contrato admite solo YAML plano de escalares, sin dependencias.
        values = {}
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                match = re.fullmatch(r"([a-z_]+):\s*(.*?)\s*", line)
                if not match or match[1] in values:
                    raise ValueError("se esperaba YAML plano sin claves duplicadas")
                value = re.split(r"\s+#", match[2], maxsplit=1)[0].strip()
                if value.startswith(('"', "'")):
                    if len(value) < 2 or value[-1] != value[0]:
                        raise ValueError("comillas sin cerrar")
                    value = value[1:-1]
                values[match[1]] = value
            url = values["mcp_url"].rstrip("/")
            parsed = urlsplit(url)
            if (parsed.scheme not in ("http", "https") or not parsed.hostname
                    or parsed.username or parsed.password or parsed.query or parsed.fragment
                    or parsed.path):
                raise ValueError("mcp_url debe ser el origen HTTP(S) de la API")
            _ = parsed.port
            organization = str(UUID(values["organization_id"]))
            repository = str(UUID(values["repository_id"]))
        except (OSError, ValueError, KeyError) as exc:
            raise GeasError("CONFIG", f".geas.yml inválida: {exc}") from exc
        actor = os.environ.get("GEAS_ACTOR_ID") or os.environ.get("GEAS_ACTOR", "")
        try:
            actor = str(UUID(actor))
        except ValueError as exc:
            raise GeasError("ACTOR_REQUIRED", "Exporta GEAS_ACTOR_ID con tu UUID personal.") from exc
        return cls(url, organization, repository, actor)

    def request(self, path: str, params: dict | None = None) -> dict:
        request = Request(
            self.url + path,
            data=None if params is None else json.dumps(params).encode(),
            headers={"Content-Type": "application/json", "X-Geas-Actor": self.actor_id,
                     "X-Geas-Organization": self.organization_id},
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read()
        except HTTPError as exc:
            try:
                detail = json.loads(exc.read()).get("error", exc.reason)
            except (ValueError, AttributeError):
                detail = exc.reason
            raise GeasError("HTTP", f"GEAS HTTP {exc.code}: {detail}") from exc
        except (URLError, OSError, HTTPException) as exc:
            raise GeasError("NETWORK", f"GEAS inaccesible/timeout: {exc}") from exc
        try:
            payload = json.loads(body)
        except (ValueError, UnicodeError) as exc:
            raise GeasError("PROTOCOL", "GEAS devolvió JSON malformado.") from exc
        if not isinstance(payload, dict):
            raise GeasError("PROTOCOL", "GEAS debe devolver un objeto JSON.")
        return payload

    def call(self, tool: str, **params) -> dict:
        payload = self.request("/api/tools/" + tool, params)
        if payload.get("success") is not True:
            raise GeasError("REMOTE", f"GEAS {tool}: {payload.get('error', 'sin success=true')}")
        data = payload.get("data")
        if not isinstance(data, dict):
            raise GeasError("PROTOCOL", f"GEAS {tool}: data no es un objeto.")
        return data

    def context(self) -> dict:
        if self.request("/health").get("status") != "ok":
            raise GeasError("HEALTH", "GEAS no está sano.")
        repos = self.call("list_repositories", organization_id=self.organization_id)
        repositories = repos.get("repositories")
        if not isinstance(repositories, list) or not all(isinstance(r, dict) for r in repositories):
            raise GeasError("PROTOCOL", "Lista de repositorios GEAS inválida.")
        if (repos.get("organization_id") != self.organization_id
                or not any(r.get("id") == self.repository_id for r in repositories)):
            raise GeasError("REPOSITORY", "Repositorio fuera de la organización configurada.")
        context = self.call("get_repository_context", repository_id=self.repository_id)
        if (context.get("id") != self.repository_id or not isinstance(context.get("tickets"), list)
                or not all(isinstance(t, dict) for t in context["tickets"])):
            raise GeasError("PROTOCOL", "Contexto GEAS de repositorio inválido.")
        return context

    def ticket(self, ticket_id: str) -> dict:
        # get_ticket upstream no incluye repository_id: comprobar pertenencia
        # usando el contexto autorizado, nunca inferirla del título.
        context = self.call("get_repository_context", repository_id=self.repository_id)
        tickets = context.get("tickets")
        if (context.get("id") != self.repository_id or not isinstance(tickets, list)
                or not all(isinstance(t, dict) for t in tickets)):
            raise GeasError("PROTOCOL", "Contexto de tickets inválido.")
        if not any(t.get("id") == ticket_id for t in tickets):
            raise GeasError("TICKET", "Ticket ausente del repositorio configurado.")
        ticket = self.call("get_ticket", ticket_id=ticket_id)
        if ticket.get("id") != ticket_id:
            raise GeasError("PROTOCOL", "GEAS devolvió otro ticket.")
        return ticket

    def owned(self, ticket: dict, status: str, sha: str, field: str) -> None:
        if (not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40,64}", sha)
                or ticket.get("status") != status or ticket.get("assigned_actor_id") != self.actor_id
                or ticket.get(field) != sha):
            raise GeasError("OWNERSHIP", f"No se verificó {status}, actor y {field}={sha} en GEAS.")

    def claim(self, ticket_id: str, head: str) -> dict:
        ticket = self.ticket(ticket_id)
        if ticket.get("status") == "IN_PROGRESS":
            # Retomar conserva el SHA original, que debe ser un commit válido.
            before = ticket.get("commit_before", "")
            if not isinstance(before, str) or not re.fullmatch(r"[0-9a-f]{40,64}", before):
                raise GeasError("PROTOCOL", "Ticket reclamado sin commit_before válido.")
            self.owned(ticket, "IN_PROGRESS", before, "commit_before")
            return ticket
        if ticket.get("status") != "FREE" or ticket.get("assigned_actor_id") not in (None, "", self.actor_id):
            raise GeasError("OWNERSHIP", "Ticket no está libre o pertenece a otro actor.")
        try:
            self.call("start_ticket", ticket_id=ticket_id, commit_before=head)
        except GeasError:
            # La respuesta puede perderse DESPUÉS del CAS. Nunca repetir el
            # claim a ciegas ni confiar en el success del MCP upstream.
            ticket = self.ticket(ticket_id)
            self.owned(ticket, "IN_PROGRESS", head, "commit_before")
            return ticket
        ticket = self.ticket(ticket_id)
        self.owned(ticket, "IN_PROGRESS", head, "commit_before")
        return ticket

    def complete(self, ticket_id: str, head: str, evidence: str) -> None:
        ticket = self.ticket(ticket_id)
        if ticket.get("status") == "DONE":
            self.owned(ticket, "DONE", head, "commit_after")
            return
        self.owned(ticket, "IN_PROGRESS", ticket.get("commit_before"), "commit_before")
        try:
            self.call("complete_ticket", ticket_id=ticket_id, commit_after=head, result=evidence)
        except GeasError:
            self.owned(self.ticket(ticket_id), "DONE", head, "commit_after")
            return
        self.owned(self.ticket(ticket_id), "DONE", head, "commit_after")
