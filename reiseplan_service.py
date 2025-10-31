import json

def lade_bausteine():
    with open("data/bausteine.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def erzeuge_reiseplan(route_chain):
    bausteine = lade_bausteine()
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
        elif b["type"].startswith("route"):
            start_idx = route_chain.index(b["start_ort"].lower())
            return (start_idx + 0.5, 1)
        return (999, 2)

    plan = sorted(unique_plan, key=sort_key)

    print(f"Reiseplan erstellt: {len(plan)} Bausteine gefunden")
    for p in plan:
        print(f" - {p['title']} ({p['type']})")

    return plan
