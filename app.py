import json
from flask import Flask, render_template, request

app = Flask(__name__)


def lade_bausteine():
    with open("data/bausteine.json", "r", encoding="utf-8") as f:
        return json.load(f)
    

@app.route("/reiseplan", methods=["GET", "POST"])
def reiseplan():

    tage = request.form.get("tage") or request.args.get("tage") or "0"
    thema = request.form.get("thema") or request.args.get("thema") or "unbekannt"
    route = request.form.get("route") or request.args.get("route") or "unbekannt"

    bausteine = lade_bausteine()
    plan = [b for b in bausteine if b["route"] == route and b["thema"] == thema]


    return render_template("reiseplan.html", plan=plan, thema=thema, route=route, tage=tage)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
