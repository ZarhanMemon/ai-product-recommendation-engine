from flask import Flask, render_template, request
from recommender import recommend_products
import pandas as pd
import os

app = Flask(__name__)

# Load unique users for dropdown
df = pd.read_csv("users_order.csv", encoding="utf-8")
users = df["customer_id"].unique()

@app.route("/")
def index():
    return render_template("index.html", users=users)

@app.route("/recommend", methods=["POST"])
def recommend():
    user_id = request.form["user_id"]
    bought, recommended = recommend_products(user_id)

    return render_template(
        "recommendations.html",
        user_id=user_id,
        bought=bought,
        recommended=recommended
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

