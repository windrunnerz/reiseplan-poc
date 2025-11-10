from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from src.reiseplan_service import lade_bausteine, erzeuge_reiseplan, build_graph, finde_route_pfad, finde_alle_erreichbaren_ziele
from src.config import TEMPLATE_DIR, STATIC_DIR, DATA_FILE
import json

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
)
app.secret_key = "supersecretkey"

def get_demo_pfad():
    """Erzeugt den Demo-Pfad für die Sidebar."""
    bausteine = lade_bausteine()
    graph = build_graph(bausteine)
    demo_start = "Stege"
    demo_ziel = "Vemb"
    demo_pfad = finde_route_pfad(demo_start.lower(), demo_ziel.lower(), graph)
    return demo_pfad

def get_orte():
    """Lädt Bausteine und gibt Start-, Ziel- und City-Orte sortiert zurück."""
    bausteine = lade_bausteine()

    routen = [b for b in bausteine if b["type"].startswith("route_")]
    cities = [b for b in bausteine if b["type"] == "city"]

    start_orte = sorted({b["start_ort"] for b in routen})
    ziel_orte = sorted({b["ziel_ort"] for b in routen})
    stadt_orte = sorted({b["ort"] for b in cities})

    return start_orte, ziel_orte, stadt_orte

@app.route("/api/ziele")
def api_ziele():
    start = request.args.get("start", "").lower()
    bausteine = lade_bausteine()
    graph = build_graph(bausteine)

    ziele = finde_alle_erreichbaren_ziele(start, graph)
    print(f"🔍 Mögliche Ziele von {start}: {ziele}")

    return jsonify(sorted([z.title() for z in ziele]))

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
    print("RAW POST:", dict(request.form))

    if request.method == "POST":
        form_data = request.form.to_dict()
        print("📨 Neues Formular erhalten:")
        for key, value in form_data.items():
            print(f" - {key}: {value}")

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                bausteine = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            bausteine = []

        # Neuer Eintrag basierend auf Typ
        if form_data.get("type") == "city":
            print("city Baustein")
            neuer_baustein = {
                "id": f"city_{len(bausteine)+1}",
                "type": "city",
                "title": form_data.get("ort", "Unbenannter Ort"),
                "text": form_data.get("city_text", ""),
                "ort": form_data.get("ort"),
                "image": form_data.get("image", None),
                "sehenswuerdigkeiten": []
            }
        else:
            print("route Baustein")
            neuer_baustein = {
                "id": f"route_{len(bausteine)+1}",
                "type": "route_simple",
                "title": f"{form_data.get('start_ort','')} – {form_data.get('ziel_ort','')}",
                "text": form_data.get("route_text", ""),
                "start_ort": form_data.get("start_ort"),
                "ziel_ort": form_data.get("ziel_ort"),
                "image": None
            }

        bausteine.append(neuer_baustein)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(bausteine, f, indent=2, ensure_ascii=False)

        print(f"✅ Neuer Baustein gespeichert ({neuer_baustein['id']})")
        flash("✅ Neuer Baustein erfolgreich gespeichert.")
        return redirect(url_for("index"))

    # GET → Formular anzeigen
    start_orte, ziel_orte, stadt_orte = get_orte()

    # Alle City-Orte für die Dropdowns anzeigen
    return render_template(
        "add_baustein.html",
        start_orte=stadt_orte,
        ziel_orte=stadt_orte,
        stadt_orte=stadt_orte,
        demo_pfad=get_demo_pfad()
    )

@app.route("/")
def index():
    """
    Startseite: zeigt die Eingabemaske zur Routenerstellung.
    Start-Orte werden direkt übergeben, Ziel-Orte werden dynamisch per API geladen.
    """
    bausteine = lade_bausteine()
    graph = build_graph(bausteine)

    start_orte = sorted([s.title() for s in graph.keys()])

    return render_template(
        "index.html",
        start_orte=start_orte,
        demo_pfad=get_demo_pfad()
    )

if __name__ == "__main__":
    app.run(debug=True)
