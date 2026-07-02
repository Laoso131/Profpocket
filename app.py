from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


# 🔥 EXEMPLE SEARCH ROUTE (corrige ton bouton recherche)
@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "empty query"}), 400

    # MOCK RESULT (remplace par ton IA plus tard)
    return jsonify({
        "result": f"Résultat pour: {query}"
    })


# 🔥 IMPORTANT RAILWAY FIX
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return "Dashboard OK"

@app.route("/login")
def login():
    return "Login OK"

if __name__ == "__main__":
    app.run()
