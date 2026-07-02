from flask import Flask, request, jsonify, render_template, session
import sqlite3
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "secret_key_change_me"

# =========================
# 🧠 DATABASE MEMORY
# =========================
def init_db():
    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT,
            response TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# 🌐 AI (OPENROUTER = INTERNET + GPT)
# =========================
API_KEY = "PUT_YOUR_API_KEY_HERE"

def ai_response(user_message, history=[]):

    system = """
Tu es une IA type ChatGPT.
Tu expliques clairement comme un professeur.
Tu peux répondre à toutes les matières scolaires.
Sois structuré, précis et utile.
"""

    messages = [{"role": "system", "content": system}]

    for h in history[-5:]:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})

    messages.append({"role": "user", "content": user_message})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": messages
        }
    )

    return response.json()["choices"][0]["message"]["content"]

# =========================
# 🏠 HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# 💬 CHAT + MEMORY
# =========================
@app.route("/chat", methods=["POST"])
def chat():

    msg = request.json.get("message")
    user = session.get("user", "guest")

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("SELECT message, response FROM messages WHERE user=? ORDER BY id DESC LIMIT 5", (user,))
    history = c.fetchall()

    reply = ai_response(msg, history)

    c.execute(
        "INSERT INTO messages (user, message, response) VALUES (?,?,?)",
        (user, msg, reply)
    )

    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

# =========================
# 🔐 SIMPLE LOGIN (OPTION)
# =========================
@app.route("/login", methods=["POST"])
def login():
    session["user"] = request.json.get("username")
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
