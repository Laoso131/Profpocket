from flask import Flask, request, jsonify, session, render_template, redirect

app = Flask(__name__)
app.secret_key = "change_me"

# ======================
# HOME (protégé)
# ======================
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return "<h1>HOME OK</h1>"

# ======================
# LOGIN PAGE (GET)
# ======================
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# ======================
# LOGIN API (POST)
# ======================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    u = data.get("username")
    p = data.get("password")

    # TEST SIMPLE (sans DB pour éviter bugs)
    if u == "admin" and p == "1234":
        session["user"] = u
        return jsonify({"msg": "ok"})

    return jsonify({"msg": "error"})

# ======================
# REGISTER API
# ======================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    u = data.get("username")
    p = data.get("password")

    # DEMO SIMPLE
    return jsonify({"msg": "created"})

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
