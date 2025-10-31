from flask import Flask, render_template, request
from reiseplan_service import lade_bausteine, erzeuge_reiseplan

app = Flask(__name__)

@app.route("/reiseplan", methods=["GET", "POST"])
def reiseplan():
    start = request.form.get("start") or request.args.get("start") or "unbekannt"
    ziel = request.form.get("ziel") or request.args.get("ziel") or "unbekannt"
    zwischenstopps = request.form.getlist("zwischenstopps") or request.args.getlist("zwischenstopps") or []
    reiseart = request.form.get("reiseart") or request.args.get("reiseart") or "unbekannt"
    tage = request.form.get("tage") or request.args.get("tage") or "0"

    route_chain = [start.lower()] + [s.lower() for s in zwischenstopps] + [ziel.lower()]

    plan = erzeuge_reiseplan(route_chain)

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
