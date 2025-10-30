from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Willkommen beim Reiseplan-PoC 🌍</h1><p>Flask läuft erfolgreich!</p>"

if __name__ == "__main__":
    app.run(debug=True)
