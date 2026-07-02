from flask import Flask, request, jsonify, render_template, session
import sqlite3

app = Flask(__name__)
app.secret_key = "profpocket_secret"

# 🧠 IA CORE
def ai(msg):
    msg = msg.lower()

    if "dérivé" in msg:
        return "📘 f(x)=x² → f'(x)=2x"
    if "physique" in msg:
        return "⚡ F = m × a"
    if "chimie" in msg:
        return "🧪 H2 + O2 → H2O"
    
    return "🤖 ProfPocket SaaS : pose une question plus précise."

# 🗄️ DB INIT
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

# 🤖 CHAT IA
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message")

    return jsonify({"reply": ai(msg)})

# 👤 REGISTER SIMPLE
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    u = data["username"]
    p = data["password"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?,?)", (u,p))
    conn.commit()
    conn.close()

    return jsonify({"msg": "user created"})

# 🔐 LOGIN SIMPLE
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    u = data["username"]
    p = data["password"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
    user = c.fetchone()
    conn.close()

    if user:
        session["user"] = u
        return jsonify({"msg": "ok"})
    return jsonify({"msg": "error"})

if __name__ == "__main__":
    app.run(debug=True)
