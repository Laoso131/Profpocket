from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)

users = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signin", methods=["POST"])
def signin():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False})

    users[email] = password

    return jsonify({
        "success": True
    })

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    msg = data.get("message", "")

    return jsonify({
        "reply":
        f"ProfPocket : Je peux t'aider sur → {msg}"
    })

@app.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return jsonify({
            "success": False
        })

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "success": False
        })

    path = os.path.join(
        "uploads",
        file.filename
    )

    file.save(path)

    return jsonify({
        "success": True
    })

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
