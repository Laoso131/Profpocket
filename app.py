import os
from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es ProfPocket, une IA pour élèves de lycée qui explique simplement."},
            {"role": "user", "content": msg}
        ]
    )

    return jsonify({
        "reply": response.choices[0].message.content
    })
