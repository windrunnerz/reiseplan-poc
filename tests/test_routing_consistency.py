import pytest
from src.reiseplan_service import build_graph, finde_route_pfad, lade_bausteine


# 🔹 Test 1: Jede Route verweist auf existierende Citys
def test_routes_reference_existing_cities():
    data = lade_bausteine()

    cities = {b["ort"].lower() for b in data if b["type"] == "city"}
    routes = [b for b in data if b["type"].startswith("route_")]

    for route in routes:
        start = (route.get("start_ort") or "").lower()
        ziel = (route.get("ziel_ort") or "").lower()
        assert start in cities, f"Ungültiger Startort: {start} (in {route['id']})"
        assert ziel in cities, f"Ungültiger Zielort: {ziel} (in {route['id']})"


# 🔹 Test 2: Der Graph kann erfolgreich gebaut werden
def test_graph_builds_successfully():
    data = lade_bausteine()
    graph = build_graph(data)

    # Sicherstellen, dass alle Keys auch im Graph auftauchen
    assert isinstance(graph, dict), "Graph sollte ein Dictionary sein"
    assert len(graph) > 0, "Graph ist leer"
    for node, neighbors in graph.items():
        assert isinstance(neighbors, list), f"Nachbarn von {node} sind kein Array"


# 🔹 Test 3: Jede Route ist im Graph erreichbar
@pytest.mark.parametrize("bidirectional", [True, False])
def test_each_route_is_reachable(bidirectional):
    """
    Prüft, dass jede definierte Route (start → ziel) im Graph erreichbar ist.
    Mit bidirectional=True wird auch die Umkehrverbindung getestet.
    """
    data = lade_bausteine()
    graph = build_graph(data)

    for route in [b for b in data if b["type"].startswith("route_")]:
        start = route["start_ort"].lower()
        ziel = route["ziel_ort"].lower()

        path = finde_route_pfad(graph=graph, start=start, ziel=ziel)
        assert path is not None, f"Keine Verbindung gefunden: {start} → {ziel}"

        if bidirectional:
            reverse = finde_route_pfad(graph=graph, ziel=ziel, start=start)
            assert reverse is not None, f"Keine Rückverbindung: {ziel} → {start}"
