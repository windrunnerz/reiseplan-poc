import json
from pathlib import Path
import pytest

def load_bausteine():
    path = Path("data/bausteine.json")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def test_json_can_be_loaded():
    data = load_bausteine()
    assert isinstance(data, list), "JSON sollte eine Liste sein"
    assert len(data) > 0, "bausteine.json ist leer"


def test_each_entry_has_type():
    data = load_bausteine()
    for item in data:
        assert "type" in item, f"Eintrag ohne 'type': {item}"
        assert item["type"] in ["city", "route_simple", "route_detailed"], \
            f"Unbekannter Typ: {item['type']}"


def test_required_fields_by_type():
    data = load_bausteine()
    for item in data:
        t = item["type"]

        if t == "city":
            assert "ort" in item and item["ort"], f"City ohne Ort: {item.get('id')}"

        elif t.startswith("route_"):
            assert all(k in item for k in ["start_ort", "ziel_ort"]), \
                f"Route unvollständig: {item.get('id')}"
            assert item["start_ort"] and item["ziel_ort"], \
                f"Leere Ortsfelder in {item.get('id')}"


def test_unique_ids():
    data = load_bausteine()
    ids = [item["id"] for item in data if "id" in item]
    assert len(ids) == len(set(ids)), "Doppelte IDs gefunden"
