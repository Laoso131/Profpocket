from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
import requests
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_KEY"

# =========================
# 🔐 GOOGLE AUTH
# =========================
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)

# =========================
# 💾 DB
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
# 🧠 IA (OpenRouter)
# =========================
API_KEY = "YOUR_OPENROUTER_KEY"

def ask_ai(message, history):

    msgs = [{"role": "system", "content": "Tu es une IA utile, claire et éducative."}]

    for h in history[-6:]:
        msgs.append({"role": "user", "content": h[0]})
        msgs.append({"role": "assistant", "content": h[1]})

    msgs.append({"role": "user", "content": message})

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={"model": "gpt-4o-mini", "messages": msgs}
    )

    return r.json()["choices"][0]["message"]["content"]

# =========================
# 🏠 HOME
# =========================
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

# =========================
# 🔐 LOGIN PAGE
# =========================
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/email", methods=["POST"])
def login_email():
    session["user"] = request.json["email"]
    return jsonify({"ok": True})

# =========================
# 🔑 GOOGLE LOGIN
# =========================
@app.route("/login/google")
def login_google():
    return google.authorize_redirect("http://localhost:5000/auth/callback")

@app.route("/auth/callback")
def callback():
    token = google.authorize_access_token()
    user = google.get("userinfo").json()
    session["user"] = user["email"]
    return redirect("/")

# =========================
# 💬 CHAT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    user = session.get("user")
    msg = request.json["message"]

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("SELECT message, response FROM messages WHERE user=? ORDER BY id DESC LIMIT 6", (user,))
    history = c.fetchall()

    reply = ask_ai(msg, history)

    c.execute("INSERT INTO messages VALUES (NULL,?,?,?)", (user, msg, reply))

    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

# =========================
# 📜 HISTORY
# =========================
@app.route("/history")
def history():
    user = session.get("user")

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("SELECT message, response FROM messages WHERE user=? ORDER BY id DESC", (user,))
    data = c.fetchall()

    return jsonify(data)

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run()
    
