from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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

@app.route("/api/moegliche_routen")
def api_moegliche_routen():
    start = request.args.get("start", "").lower()
    ziel = request.args.get("ziel", "").lower()

    bausteine = lade_bausteine()
    graph = build_graph(bausteine)

    alle_pfade = finde_route_pfad(start, ziel, graph, alle=True)
    if not alle_pfade:
        return jsonify([])

    print(f"🔍 Gefundene Pfade von {start} nach {ziel}: {alle_pfade}")

     # Pfade in lesbare Strings umwandeln
    pfad_strings = [" → ".join([ort.title() for ort in pfad]) for pfad in alle_pfade]
    return jsonify(pfad_strings)

@app.route("/reiseplan", methods=["GET", "POST"])
def reiseplan():
    """
    Flask-Route zur Erstellung eines vollständigen Reiseplans basierend auf Benutzereingaben.

    Der Benutzer kann entweder eine vollständige Route (Radiobutton-Auswahl) wählen 
    oder nur Start- und Zielort angeben. 
    Wird eine Route ausgewählt, wird deren Reihenfolge direkt übernommen und der Reiseplan 
    auf Basis der entsprechenden Bausteine erzeugt.

    Wird keine Route ausgewählt, erfolgt die automatische Berechnung der route_chain 
    per Tiefensuche (DFS) im aus den JSON-Bausteinen generierten Graphen.

    Das Ergebnis - also alle passenden City- und Routen-Bausteine entlang der ermittelten 
    Strecke - wird anschließend im Template reiseplan.html dargestellt.
    """

    start = request.form.get("start") or request.args.get("start") or "unbekannt"
    ziel = request.form.get("ziel") or request.args.get("ziel") or "unbekannt"

    moegliche_route = request.form.get("moegliche_route") or request.args.get("moegliche_route")

    bausteine = lade_bausteine()
    graph = build_graph(bausteine)

    if moegliche_route:
        route_chain = [ort.strip().lower() for ort in moegliche_route.split("→")]
        mode = "auswahl"
        print(f"🧭 Ausgewählte Route: {' → '.join(route_chain)}")

    else:
        route_chain = finde_route_pfad(start.lower(), ziel.lower(), graph)
        mode = "auto"

    print(f"🗺️ Mode: {mode}, Route chain: {route_chain}")

    plan = erzeuge_reiseplan(route_chain, bausteine)

    return render_template(
        "reiseplan.html",
        plan=plan,
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
    bausteine = lade_bausteine()
    graph = build_graph(bausteine)

    demo_start = "Stege"
    demo_ziel = "Vemb"
    demo_pfad = finde_route_pfad(demo_start.lower(), demo_ziel.lower(), graph)

    moegliche_stopps = demo_pfad[1:-1] if demo_pfad else []

    return render_template(
        "index.html",
        start_orte=start_orte,
        ziel_orte=ziel_orte,
        stadt_orte=stadt_orte,
        moegliche_stopps=moegliche_stopps,
        demo_pfad=demo_pfad
    )

if __name__ == "__main__":
    app.run(debug=True)
