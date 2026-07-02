from flask import Flask, request, jsonify, session, render_template, redirect, Response
import sqlite3
import openai
import stripe
import time
import json

app = Flask(__name__)
app.secret_key = "CHANGE_ME_SUPER_SECRET"

# ======================
# KEYS
# ======================
openai.api_key = "OPENAI_KEY"
stripe.api_key = "STRIPE_SECRET_KEY"

# Stripe product (à créer dans Stripe dashboard)
PRICE_ID = "price_xxxxxxxxxxxxx"

# ======================
# DB
# ======================
def init_db():
    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        plan TEXT DEFAULT 'free'
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
# AUTH
# ======================
def logged():
    return "user" in session

# ======================
# LOGIN / REGISTER (simple)
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

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    u = data["username"]
    p = data["password"]

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username,password) VALUES (?,?)", (u,p))
        conn.commit()
    except:
        return jsonify({"msg":"exists"})

    conn.close()
    return jsonify({"msg":"created"})

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

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("SELECT plan FROM users WHERE username=?", (session["user"],))
    plan = c.fetchone()

    conn.close()

    return render_template("dashboard.html",
        user=session["user"],
        plan=plan[0] if plan else "free"
    )

# ======================
# STRIPE CHECKOUT
# ======================
@app.route("/subscribe")
def subscribe():

    checkout = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": PRICE_ID,
            "quantity": 1,
        }],
        mode="subscription",
        success_url="http://localhost:5000/dashboard",
        cancel_url="http://localhost:5000/dashboard",
    )

    return redirect(checkout.url)

# ======================
# STREAMING AI (CHATGPT STYLE)
# ======================
@app.route("/stream", methods=["POST"])
def stream():

    if not logged():
        return "not logged"

    data = request.get_json()
    msg = data["message"]

    def generate():

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user","content":msg}],
                stream=True
            )

            for chunk in response:
                if "content" in chunk["choices"][0]["delta"]:
                    token = chunk["choices"][0]["delta"]["content"]
                    yield f"data: {json.dumps(token)}\n\n"
                    time.sleep(0.01)

        except:
            yield "data: error\n\n"

    return Response(generate(), mimetype="text/event-stream")

# ======================
# CHAT NORMAL (fallback)
# ======================
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    msg = data["message"]

    return jsonify({"reply": "Use streaming endpoint /stream"})

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)
