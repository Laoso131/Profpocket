from flask import Flask, request, jsonify, session, render_template, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "change_me"

# ======================
# DATABASE
# ======================
def init_db():
    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

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
# LOGIN API
# ======================
@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = c.fetchone()

    conn.close()

    if user:
        session["user"] = username
        return jsonify({"msg":"ok"})

    return jsonify({"msg":"error"})

# ======================
# REGISTER API
# ======================
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("db.db")
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"msg":"exists"})

    conn.close()

    return jsonify({"msg":"created"})

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
def is_admin():
    return session.get("user") == "admin"
