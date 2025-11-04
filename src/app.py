from flask import Flask, render_template, request, redirect, url_for, flash
from src.reiseplan_service import lade_bausteine, erzeuge_reiseplan, build_graph, finde_route_pfad
from src.config import TEMPLATE_DIR, STATIC_DIR

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
)
app.secret_key = "supersecretkey"

def get_orte():
    """Lädt Bausteine und gibt Start-, Ziel- und City-Orte sortiert zurück."""
    bausteine = lade_bausteine()

    routen = [b for b in bausteine if b["type"].startswith("route_")]
    cities = [b for b in bausteine if b["type"] == "city"]

    start_orte = sorted({b["start_ort"] for b in routen})
    ziel_orte = sorted({b["ziel_ort"] for b in routen})
    stadt_orte = sorted({b["ort"] for b in cities})

    return start_orte, ziel_orte, stadt_orte

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

@app.route("/add_baustein", methods=["GET", "POST"])
def add_baustein():
    if request.method == "POST":
        form_data = request.form.to_dict()
        print("📨 Neues Formular erhalten:")
        for key, value in form_data.items():
            print(f" - {key}: {value}")

        flash("✅ Neuer Baustein erfolgreich gespeichert.")
        return redirect(url_for("index"))
    
    # GET → Formular anzeigen
    start_orte, ziel_orte, stadt_orte = get_orte()
    return render_template(
        "add_baustein.html",
        start_orte=start_orte,
        ziel_orte=ziel_orte,
        stadt_orte=stadt_orte
    )

@app.route("/")
def index():   
    start_orte, ziel_orte, stadt_orte = get_orte()
    return render_template(
        "index.html",
        start_orte=start_orte,
        ziel_orte=ziel_orte,
        stadt_orte=stadt_orte
    )

if __name__ == "__main__":
    app.run(debug=True)
