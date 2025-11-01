import json

def lade_bausteine():
    with open("data/bausteine.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def erzeuge_reiseplan(route_chain, bausteine):
    """
    Erzeugt den vollständigen Reiseplan aus den vorhandenen Bausteinen und der route_chain.

    Durchsucht alle City- und Routen-Bausteine nach passenden Einträgen entlang der route_chain 
    (Start → Zwischenstopps → Ziel) und kombiniert sie zu einem zusammenhängenden Reiseplan.
    Doppelte Einträge werden entfernt, anschließend erfolgt eine chronologische Sortierung 
    entsprechend der Reihenfolge in route_chain. 

    Rückgabe:
        Eine sortierte Liste aller relevanten Bausteine (Städte und Routen) für die gewählte Reise.
    """

    plan = []

    # 1️⃣  Alle passenden City-Bausteine holen
    for b in bausteine:
        if b.get("type") == "city" and b.get("ort"):
            ort = b["ort"].lower()
            if ort in route_chain:
                plan.append(b)

    # 2️⃣  Alle Routen holen, die genau zwischen zwei aufeinanderfolgenden Orten liegen
    for b in bausteine:
        if not b.get("type", "").startswith("route"):
            continue

        start_ort = (b.get("start_ort") or "").lower()
        ziel_ort = (b.get("ziel_ort") or "").lower()

        # alle Paare aus der Reihenfolge bilden: [(stege,kopenhagen), (kopenhagen,vemb)]
        for s, z in zip(route_chain, route_chain[1:]):
            if start_ort == s and ziel_ort == z:
                plan.append(b)

    # 3️⃣ Keine Ergebnisse? -> Nichts zurückgeben
    if not plan:
        print("⚠️ Keine passenden Routen gefunden.")
        return []

    # 3️⃣  Duplikate entfernen
    unique_plan = []
    seen_ids = set()
    for b in plan:
        if b["id"] not in seen_ids:
            unique_plan.append(b)
            seen_ids.add(b["id"])

    # 4️⃣  Chronologisch sortieren nach der Reihenfolge in route_chain
    def sort_key(b):
        if b["type"] == "city":
            ort = b.get("ort", "").lower()
            return (route_chain.index(ort), 0)
        if b["type"].startswith("route"):
            start_idx = route_chain.index(b["start_ort"].lower())
            return (start_idx + 0.5, 1)
        return (999, 2)

    plan = sorted(unique_plan, key=sort_key)

    print(f"Reiseplan erstellt: {len(plan)} Bausteine gefunden")
    for p in plan:
        print(f" - {p['title']} ({p['type']})")

    return plan

def build_graph(bausteine):
    """
    Baut ein Graph-Mapping aus den gegebenen Bausteinen auf.
    Ergebnis: dict mit allen Orten als Keys und deren erreichbaren Zielorten als Values.

    Beispiel:
        {
            "Stege": ["Kopenhagen"],
            "Kopenhagen": ["Vemb", "Malmö"],
            "Malmö": ["Kopenhagen"],
            "Vemb": []
        }
    """

    graph = {}

    # 1️⃣ Alle City-Bausteine initialisieren (Knoten ohne Verbindungen)
    for b in bausteine:
        if b.get("type") == "city" and b.get("ort"):
            ort = b["ort"].strip().lower() # z. B. 'kopenhagen' -> 'Kopenhagen'
            if ort not in graph:
                graph[ort] = []

    # 2️⃣ Alle Routen auswerten (gerichtete Kanten)
    for b in bausteine:
        if not b.get("type", "").startswith("route"):
            continue

        start_ort = (b.get("start_ort") or "").strip().lower()
        ziel_ort = (b.get("ziel_ort") or "").strip().lower()

        # Sicherheitscheck: ungültige oder leere Routen überspringen
        if not start_ort or not ziel_ort:
            continue

        # Falls Start-Ort noch nicht existiert (z. B. City fehlt)
        if start_ort not in graph:
            graph[start_ort] = []

        # Ziel-Ort zu Start-Ort hinzufügen, wenn nicht schon vorhanden
        if ziel_ort not in graph[start_ort]:
            graph[start_ort].append(ziel_ort)

        # Sicherstellen, dass Ziel-Ort als Key existiert (Schritt 5)
        if ziel_ort not in graph:
            graph[ziel_ort] = []

    # 3️⃣ Optional: Logging / Debug-Ausgabe
    print("📍 Generierter Graph:")
    for ort, nachbarn in graph.items():
        print(f"  {ort} → {nachbarn}")

    return graph

def finde_route_pfad(start, ziel, graph, pfad=None):
    """
    Findet einen Pfad (Liste von Orten) von start → ziel im gegebenen Graphen.
    Nutzt Depth-First Search (Tiefensuche).
    Gibt None zurück, wenn kein Pfad existiert.
    """

    # 1️⃣ Erster Aufruf: leere Liste initialisieren
    if pfad is None:
        pfad = []

    # 2️⃣ Aktuellen Ort zum Pfad hinzufügen
    pfad = pfad + [start]

    # 3️⃣ Abbruchbedingung: Ziel erreicht
    if start == ziel:
        return pfad

    # 4️⃣ Keine weiteren Verbindungen → Sackgasse
    if start not in graph:
        return None

    # 5️⃣ Für alle Nachbarn (direkt erreichbare Orte)
    for nachbar in graph[start]:
        if nachbar not in pfad:  # vermeidet Zyklen
            neuer_pfad = finde_route_pfad(nachbar, ziel, graph, pfad)
            if neuer_pfad:  # sobald ein gültiger Pfad gefunden wird
                return neuer_pfad

    # 6️⃣ Kein Pfad gefunden
    return None
