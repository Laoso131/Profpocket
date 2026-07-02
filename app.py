from flask import Flask, request, jsonify, session, render_template, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"

# ======================
# DB INIT
# ======================
def init_db():
    conn = sqlite3.connect("db.db")
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
        user TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ======================
# REGISTER
# ======================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    u = data.get("username")
    p = data.get("password")

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?,?)", (u, p))
        conn.commit()
    except:
        conn.close()
        return jsonify({"msg": "exists"})

    conn.close()
    return jsonify({"msg": "created"})

# ======================
# LOGIN
# ======================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    u = data.get("username")
    p = data.get("password")

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    user = c.fetchone()

    conn.close()

    if user:
        session["user"] = u
        return jsonify({"msg": "ok"})

    return jsonify({"msg": "error"})

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ======================
# PROTECTION ROUTE
# ======================
def require_login():
    if "user" not in session:
        return False
    return True

# ======================
# HOME
# ======================
@app.route("/")
def home():
    if not require_login():
        return redirect("/login")

    return render_template("index.html", user=session["user"])

# ======================
# LOGIN PAGE
# ======================
@app.route("/login")
def login_page():
    return render_template("login.html")

# ======================
# REGISTER PAGE
# ======================
@app.route("/register-page")
def register_page():
    return render_template("register.html")

# ======================
# 🧠 IA CORE (AMÉLIORÉE)
# ======================
def ai_engine(msg):

    msg = msg.lower()

    # maths
    if "derive" in msg or "dérivé" in msg:
        return "📘 f(x)=x² → f'(x)=2x"

    # physics
    if "physique" in msg:
        return "⚡ F = m × a"

    # chimie
    if "chimie" in msg:
        return "🧪 H2 + O2 → H2O"

    # coding
    if "code" in msg:
        return "💻 Je peux t'aider en Python, JS, HTML, Flask"

    # general smart fallback
    return "🤖 NeoAI (beta): réponse générée localement. Bientôt connexion IA cloud."

# ======================
# CHAT IA + SAVE MESSAGE
# ======================
@app.route("/chat", methods=["POST"])
def chat():

    if not require_login():
        return jsonify({"reply": "❌ not logged in"})

    data = request.get_json()
    msg = data.get("message")

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("INSERT INTO messages (user, message) VALUES (?,?)", (session["user"], msg))
    conn.commit()
    conn.close()

    reply = ai_engine(msg)

    return jsonify({"reply": reply})

# ======================
# HISTORY (BASE SAAS FEATURE)
# ======================
@app.route("/history")
def history():

    if not require_login():
        return jsonify([])

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("SELECT message FROM messages WHERE user=?", (session["user"],))
    data = c.fetchall()

    conn.close()

    return jsonify([d[0] for d in data])

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)
