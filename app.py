from flask import Flask, request, jsonify, render_template, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "profpocket_secret_key"

# 🧠 IA SIMPLE MAIS PROPRE
def ai(msg):
    msg = msg.lower()

    if "dérivé" in msg:
        return "📘 f(x)=x² → f'(x)=2x"
    if "physique" in msg:
        return "⚡ F = m × a"
    if "chimie" in msg:
        return "🧪 H2 + O2 → H2O"

    return "🤖 Pose une question plus précise."

# 🗄️ INIT DB
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# 🏠 HOME
@app.route("/")
def home():
    return render_template("index.html")

# 🤖 CHAT + SAUVEGARDE
@app.route("import requests
from flask import request, jsonify

API_KEY = "TON_API_KEY"

def ai(message):

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "Tu es une IA qui peut répondre avec connaissances générales et infos récentes. Réponds comme ChatGPT."
                },
                {"role": "user", "content": message}
            ]
        }
    )

    return response.json()["choices"][0]["message"]["content"]

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message")
    return jsonify({"reply": ai(msg)})", methods=["POST"])
def chat():
    msg = request.json.get("message")
    user = session.get("user", "guest")

    reply = ai(msg)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (username, message) VALUES (?,?)", (user, msg))
    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

# 👤 REGISTER SECURISÉ
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    u = data["username"]
    p = generate_password_hash(data["password"])

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?,?)", (u,p))
        conn.commit()
    except:
        return jsonify({"msg": "user exists"})

    conn.close()
    return jsonify({"msg": "user created"})

# 🔐 LOGIN SECURISÉ
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    u = data["username"]
    p = data["password"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (u,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[0], p):
        session["user"] = u
        return jsonify({"msg": "ok"})

    return jsonify({"msg": "error"})

# 📜 HISTORIQUE CHAT
@app.route("/history")
def history():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT username, message FROM messages ORDER BY id DESC LIMIT 20")
    data = c.fetchall()
    conn.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
