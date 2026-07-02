from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message")

    return jsonify({
        "reply": "🤖 ProfPocket (mode gratuit): " + msg
    })
