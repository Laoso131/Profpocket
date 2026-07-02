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
# PROTECTED HOME
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
# REGISTER PAGE SIMPLE
# ======================
@app.route("/register-page")
def register_page():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
