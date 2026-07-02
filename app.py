from flask import Flask, request, jsonify, session, render_template, redirect
import sqlite3
import openai
import stripe

app = Flask(__name__)
app.secret_key = "PROPOCKET_SECRET_CHANGE_ME"

# ======================
# API KEYS (REMPLACE)
# ======================
openai.api_key = "OPENAI_KEY"
stripe.api_key = "STRIPE_KEY"

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
        role TEXT,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ======================
# AUTH CHECK
# ======================
def logged():
    return "user" in session

# ======================
# REGISTER
# ======================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    u = data["username"]
    p = data["password"]

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (NULL,?,?)", (u,p))
        conn.commit()
    except:
        return jsonify({"msg":"exists"})

    conn.close()
    return jsonify({"msg":"created"})

# ======================
# LOGIN
# ======================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    u = data["username"]
    p = data["password"]

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
    user = c.fetchone()
    conn.close()

    if user:
        session["user"] = u
        return jsonify({"msg":"ok"})
    return jsonify({"msg":"error"})

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ======================
# HOME
# ======================
@app.route("/")
def home():
    if not logged():
        return redirect("/login")
    return render_template("index.html", user=session["user"])

# ======================
# DASHBOARD
# ======================
@app.route("/dashboard")
def dashboard():
    if not logged():
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

# ======================
# 🧠 AI (OPENROUTER / OPENAI READY)
# ======================
def ai_response(msg):

    # fallback local
    if "math" in msg.lower():
        return "📘 Maths: f(x)=x² → f'(x)=2x"

    try:
        # ⚠️ remplace model si besoin
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":msg}]
        )
        return res["choices"][0]["message"]["content"]

    except:
        return "⚠️ IA offline (ajoute ta clé OpenAI)"

# ======================
# CHAT
# ======================
@app.route("/chat", methods=["POST"])
def chat():

    if not logged():
        return jsonify({"reply":"not logged"})

    data = request.get_json()
    msg = data["message"]

    reply = ai_response(msg)

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO messages VALUES (NULL,?,?,?)",
        (session["user"], "user", msg)
    )
    c.execute(
        "INSERT INTO messages VALUES (NULL,?,?,?)",
        (session["user"], "ai", reply)
    )

    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

# ======================
# HISTORY
# ======================
@app.route("/history")
def history():

    if not logged():
        return jsonify([])

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("SELECT role, content FROM messages WHERE user=?", (session["user"],))
    data = c.fetchall()

    conn.close()

    return jsonify([{"role":r,"content":c} for r,c in data])

# ======================
# STRIPE (PREMIUM READY)
# ======================
@app.route("/create-checkout-session")
def checkout():

    session_stripe = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "ProPocket AI Premium"},
                "unit_amount": 500,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:5000/dashboard",
        cancel_url="http://localhost:5000/dashboard",
    )

    return redirect(session_stripe.url)

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)
