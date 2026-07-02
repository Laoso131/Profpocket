from flask import Flask, request, jsonify, session, render_template, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "CHANGE_ME_SUPER_SECRET_KEY"

# ======================
# DATABASE INIT
# ======================
def init_db():
    conn = sqlite3.connect("profpocket.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user'
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

# ======================
# CREATE ADMIN AUTO
# ======================
def create_admin():
    conn = sqlite3.connect("profpocket.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not c.fetchone():

        c.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            ("admin", generate_password_hash("admin123"), "admin")
        )

        conn.commit()

    conn.close()

create_admin()

# ======================
# HELPERS
# ======================
def is_admin():
    return session.get("role") == "admin"

# ======================
# HOME
# ======================
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    return render_template("index.html", user=session["user"])

# ======================
# LOGIN PAGE
# ======================
@app.route("/login")
def login_page():
    return render_template("login.html")

# ======================
# REGISTER
# ======================
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    hashed = generate_password_hash(password)

    conn = sqlite3.connect("profpocket.db")
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (username, hashed, "user")
        )
        conn.commit()
    except:
        return jsonify({"msg": "exists"})

    conn.close()

    return jsonify({"msg": "created"})

# ======================
# LOGIN API
# ======================
@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("profpocket.db")
    c = conn.cursor()

    c.execute("SELECT username, password, role FROM users WHERE username=?", (username,))
    user = c.fetchone()

    conn.close()

    if user and check_password_hash(user[1], password):

        session["user"] = user[0]
        session["role"] = user[2]

        return jsonify({"msg": "ok"})

    return jsonify({"msg": "error"})

# ======================
# CHAT API (IA SIMPLE SAFE)
# ======================
@app.route("/api/chat", methods=["POST"])
def chat():

    if "user" not in session:
        return jsonify({"reply": "Not logged in"})

    data = request.get_json()
    msg = data.get("message", "").lower()

    if "hello" in msg:
        reply = "👋 Bonjour ! Je suis ProfPocket AI"
    elif "math" in msg:
        reply = "📘 Maths: x² dérivée = 2x"
    elif "ai" in msg:
        reply = "🧠 IA prête à être connectée à OpenAI / OpenRouter"
    else:
        reply = "🤖 Je suis en mode prototype. Connecte une API IA pour upgrade."

    conn = sqlite3.connect("profpocket.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages(user,message) VALUES(?,?)", (session["user"], msg))
    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

# ======================
# ADMIN
# ======================
@app.route("/admin")
def admin():

    if "user" not in session:
        return redirect("/login")

    if not is_admin():
        return "Accès refusé", 403

    conn = sqlite3.connect("profpocket.db")
    c = conn.cursor()

    c.execute("SELECT id, username FROM users")
    users = c.fetchall()

    conn.close()

    return render_template("admin.html", users=users)

# ======================
# DASHBOARD
# ======================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)
