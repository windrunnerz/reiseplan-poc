from flask import Flask, render_template, request
from src.reiseplan_service import lade_bausteine, erzeuge_reiseplan, build_graph, finde_route_pfad

app = Flask(__name__)

@app.route("/reiseplan", methods=["GET", "POST"])
def reiseplan():
    """
    Flask-Route zur Erstellung eines vollständigen Reiseplans basierend auf Benutzereingaben.

    Wenn keine Zwischenstopps angegeben sind, wird die route_chain automatisch per DFS-Pfadsuche 
    aus dem auf den JSON-Bausteinen basierenden Graphen erzeugt. 
    Sind Zwischenstopps vorhanden, wird die Reihenfolge direkt aus der Eingabe übernommen.
    Das Ergebnis (Städte und Routen) wird anschließend im Template reiseplan.html dargestellt.
    """

    start = request.form.get("start") or request.args.get("start") or "unbekannt"
    ziel = request.form.get("ziel") or request.args.get("ziel") or "unbekannt"
    zwischenstopps = (
        request.form.getlist("zwischenstopps")
        or request.args.getlist("zwischenstopps")
        or []
    )
    bausteine = lade_bausteine()
    graph = build_graph(bausteine)

    if zwischenstopps:
        route_chain = [start.lower()] + [s.lower() for s in zwischenstopps] + [ziel.lower()]
        mode = "manuell"

        # 🔍 Validierung: existieren alle Verbindungen im Graph?
        for s, z in zip(route_chain, route_chain[1:]):
            if z not in graph.get(s, []):
                print(f"❌ Ungültige Verbindung: {s} → {z}")
                return render_template(
                    "reiseplan.html",
                    plan=[],
                    error=f"Ungültige Verbindung: {s} → {z}",
                    route_chain=route_chain,
                )
            
        print(f"✅ Alle Verbindungen gültig: {' → '.join(route_chain)}")

    else:        
        route_chain = finde_route_pfad(start.lower(), ziel.lower(), graph)
        mode = "auto"

    print(f"🗺️ Mode: {mode}, Route chain: {route_chain}")

    reiseart = request.form.get("reiseart") or request.args.get("reiseart") or "unbekannt"
    tage = request.form.get("tage") or request.args.get("tage") or "0"

    plan = erzeuge_reiseplan(route_chain, bausteine)

    return render_template(
        "reiseplan.html",
        plan=plan,
        zwischenstopps=zwischenstopps,
        reiseart=reiseart,
        tage=tage,
        route_chain=route_chain
    )


@app.route("/")
def index():
    bausteine = lade_bausteine()

    start_orte = sorted({b["start_ort"] for b in bausteine if b["start_ort"]})
    ziel_orte = sorted({b["ziel_ort"] for b in bausteine if b["ziel_ort"]})
    stadt_orte = sorted({b["ort"] for b in bausteine if b["ort"]})

    return render_template(
        "index.html",
        start_orte=start_orte,
        ziel_orte=ziel_orte,
        stadt_orte=stadt_orte
    )

if __name__ == "__main__":
    app.run(debug=True)
