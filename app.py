from flask import Flask, request, jsonify, session, render_template, redirect

app = Flask(__name__)
app.secret_key = "secret_key_change_me"

# ======================
# HOME
# ======================
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

# ======================
# LOGIN PAGE (GET ONLY)
# ======================
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# ======================
# LOGIN API (POST ONLY)
# ======================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # LOGIN TEST SIMPLE (évite DB bug)
    if username == "admin" and password == "1234":
        session["user"] = username
        return jsonify({"msg": "ok"})

    return jsonify({"msg": "error"})

# ======================
# REGISTER PAGE (OPTIONNEL)
# ======================
@app.route("/register", methods=["GET"])
def register_page():
    return "<h1>Register page (optional)</h1>"

# ======================
# CHAT TEST
# ======================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")

    return jsonify({
        "reply": "🤖 AI: " + msg
    })

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
