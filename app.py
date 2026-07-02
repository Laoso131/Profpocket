from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 🧠 IA simple mais intelligente
def ai(msg):
    msg = msg.lower()

    if "math" in msg:
        return "📘 Maths : je peux t'aider sur les équations, fonctions, dérivées et probabilités."
    
    if "dérivé" in msg:
        return "📈 Une dérivée sert à mesurer une variation. Exemple : f(x)=x² → f'(x)=2x"
    
    if "physique" in msg:
        return "⚡ Physique : forces, mouvement, énergie, lois de Newton."
    
    if "chimie" in msg:
        return "🧪 Chimie : réactions chimiques, molécules, équations à équilibrer."
    
    if "bonjour" in msg:
        return "👋 Salut ! Je suis ProfPocket, ton assistant de révision."
    
    return "🤖 Je peux t'aider en maths, physique et chimie. Pose une question plus précise."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message")

    return jsonify({
        "reply": ai(msg)
    })

if __name__ == "__main__":
    app.run(debug=True)
