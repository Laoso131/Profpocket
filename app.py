import stripe

stripe.api_key = "YOUR_STRIPE_SECRET_KEY"
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# -------------------
# PAGES PRINCIPALES
# -------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


# -------------------
# API SEARCH (JS ONLY)
# -------------------

@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "empty query"}), 400

    return jsonify({
        "query": query,
        "result": f"Résultat pour: {query}"
    })


# -------------------
# HEALTH CHECK (RAILWAY)
# -------------------

@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# -------------------
# RAILWAY START
# -------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
@app.route("/create-checkout-session")
def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": "ProfPocket Premium"
                },
                "unit_amount": 500,  # 5€
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://your-site.up.railway.app/success",
        cancel_url="https://your-site.up.railway.app/cancel",
    )

    return {"url": session.url}
