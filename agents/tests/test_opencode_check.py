"""Regresiones del bloqueo de OpenCode: opciones inválidas y prompts perdidos."""

from __future__ import annotations

import json

import pytest

from agents.opencode_check import REQUIRED_AGENTS, check, main


@pytest.fixture
def opencode_project(tmp_path):
    definitions = tmp_path / ".opencode" / "agents"
    definitions.mkdir(parents=True)
    agents = {}
    for name in REQUIRED_AGENTS:
        path = definitions / f"{name}.md"
        path.write_text(f"# {name}\n\nInstrucciones de {name}.\n", encoding="utf-8")
        agents[name] = {"prompt": "{file:./" + str(path.relative_to(tmp_path)) + "}"}
    (tmp_path / "opencode.json").write_text(json.dumps({"agent": agents}), encoding="utf-8")
    return tmp_path


def test_referencias_validas_no_escriben(opencode_project):
    before = {p: p.read_bytes() for p in opencode_project.rglob("*") if p.is_file()}
    assert check(opencode_project) == []
    assert all(p.read_bytes() == text for p, text in before.items())


@pytest.mark.parametrize("filename", ["lider", "explorer", "implementer", "reviewer", "orquestador", "doc"])
def test_detecta_cada_definicion_perdida(opencode_project, filename):
    (opencode_project / ".opencode" / "agents" / f"{filename}.md").unlink()
    assert any(f"{filename}.md" in error for error in check(opencode_project))


@pytest.mark.parametrize("nested", [False, True])
def test_rechaza_instructions_que_se_reenvia_al_proveedor(opencode_project, nested):
    path = opencode_project / "opencode.json"
    config = json.loads(path.read_text())
    agent = config["agent"]["implementer"]
    target = agent.setdefault("options", {}) if nested else agent
    target["instructions"] = [".opencode/agents/implementer.md"]
    path.write_text(json.dumps(config))
    assert any("implementer" in error and "instructions" in error for error in check(opencode_project))


@pytest.mark.parametrize("prompt", [None, "", "{file:./missing.md}", "{file:./empty.md}"])
def test_detecta_prompt_que_no_se_puede_cargar(opencode_project, prompt):
    path = opencode_project / "opencode.json"
    config = json.loads(path.read_text())
    config["agent"]["doc"]["prompt"] = prompt
    path.write_text(json.dumps(config))
    (opencode_project / "empty.md").write_text(" \n")
    assert any("agent.doc:" in error for error in check(opencode_project))


@pytest.mark.parametrize("content", ["{", "[]", '{"agent": []}'])
def test_config_invalida_da_error_legible(tmp_path, content):
    (tmp_path / "opencode.json").write_text(content)
    assert any("opencode.json" in error for error in check(tmp_path))


def test_cli_falla_si_se_pierde_doc(opencode_project, monkeypatch, capsys):
    monkeypatch.chdir(opencode_project)
    assert main() == 0
    capsys.readouterr()
    (opencode_project / ".opencode" / "agents" / "doc.md").unlink()
    assert main() == 1
    assert "doc.md" in capsys.readouterr().out
