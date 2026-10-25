"""`meshharmes status` resume el backlog: camino feliz y errores de entrada."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from meshharmes.backlog import BacklogError, load_features, read_summary
from meshharmes.cli import build_parser, main


def _escribir(path: Path, features: list[dict]) -> Path:
    path.write_text(json.dumps({"features": features}), encoding="utf-8")
    return path


def test_status_real_del_repositorio(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["status"]) == 0
    salida = capsys.readouterr().out
    assert " features · " in salida
    assert "Siguiente: " in salida


def test_status_cuenta_estados_y_elige_la_siguiente(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    backlog = _escribir(
        tmp_path / "featureslist.json",
        [
            {"id": "A-001", "status": "done"},
            {"id": "A-002", "status": "pending", "depends_on": ["A-001"]},
            {"id": "A-003", "status": "pending", "depends_on": ["A-002"]},
            {"id": "A-004", "status": "blocked"},
            {"id": "A-005", "status": "in_progress"},
        ],
    )

    assert main(["status", "--backlog", str(backlog)]) == 0
    salida = capsys.readouterr().out
    assert "5 features · 2 pending · 1 in_progress · 1 done · 1 blocked" in salida
    # A-002 depende de A-001 (done); A-003 espera a A-002.
    assert "Siguiente: A-002" in salida


def test_status_sin_pendientes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    backlog = _escribir(tmp_path / "featureslist.json", [{"id": "A-001", "status": "done"}])
    assert read_summary(backlog).next_id is None
    assert main(["status", "--backlog", str(backlog)]) == 0
    assert "Siguiente: —" in capsys.readouterr().out


def test_backlog_inexistente_es_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["status", "--backlog", str(tmp_path / "no-existe.json")]) == 1
    assert "No existe el backlog" in capsys.readouterr().err


def test_backlog_no_es_json(tmp_path: Path) -> None:
    roto = tmp_path / "featureslist.json"
    roto.write_text("{no es json", encoding="utf-8")
    with pytest.raises(BacklogError, match="no es JSON válido"):
        load_features(roto)


def test_backlog_sin_lista_features(tmp_path: Path) -> None:
    vacio = tmp_path / "featureslist.json"
    vacio.write_text('{"otra_cosa": []}', encoding="utf-8")
    with pytest.raises(BacklogError, match="no tiene una lista 'features'"):
        load_features(vacio)


def test_sin_subcomando_es_error_de_uso() -> None:
    # argparse sale con código 2 en errores de uso: no lo tratamos como éxito.
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args([])
    assert exc.value.code == 2
