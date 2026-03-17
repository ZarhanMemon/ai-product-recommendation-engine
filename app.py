from flask import Flask, render_template
from recommender import recommend_products
import pandas as pd
import os

app = Flask(__name__)

# ==============================
# Load Data (Only Once)
# ==============================

orders_df = pd.read_csv("users_order.csv", encoding="utf-8")
products_df = pd.read_csv("all_products.csv", encoding="utf-8")

# Demo user (simulates logged-in user)
DEMO_USER = "U1001"


# ==============================
# Home Page (Main E-commerce Page)
# ==============================

@app.route("/")
def home():
    user_id = DEMO_USER

    # Get recommendation data
    bought, recommended = recommend_products(user_id)

    return render_template(
        "index.html",
        products=products_df.to_dict("records"),   # All products (catalog)
        recommended=recommended,                   # AI recommendations
        bought=bought                              # Previously purchased
    )


# ==============================
# Products Page (Full Catalog)
# ==============================

@app.route("/products")
def products():
    return render_template(
        "product.html",
        products=products_df.to_dict("records")
    )


# ==============================
# Demo Recommendation Page (Optional for Viva)
# ==============================

@app.route("/recommendations")
def recommendations():
    user_id = DEMO_USER

    bought, recommended = recommend_products(user_id)

    return render_template(
        "recommendations.html",
        user_id=user_id,
        bought=bought,
        recommended=recommended
    )
 

# ==============================
# Run Server

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)