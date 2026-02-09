from flask import Flask, render_template, request
from recommender import recommend_products
import pandas as pd
import os

app = Flask(__name__)

# Load unique users for dropdown
orders_df = pd.read_csv("users_order.csv", encoding="utf-8")
users = orders_df["customer_id"].unique()

@app.route("/")
def index():
    """Landing page with user dropdown"""
    return render_template("index.html", users=users)



@app.route("/recommend", methods=["POST"])
def recommend():
    """Show recommendations for selected user"""
    user_id = request.form["user_id"]
    bought, recommended = recommend_products(user_id)

    # Pass both purchased and recommended products to template
    return render_template(
        "recommendations.html",
        user_id=user_id,
        bought=bought,
        recommended=recommended
    )


@app.route("/products")
def products():
    """ show full product catalog with all fields  """
    products_df = pd.read_csv("all_products.csv", encoding="utf-8")
    return render_template("product.html", products=products_df.to_dict("records"))


@app.route("/users")
def users_list():
    """  show all users and their purchase histories  """
    orders_df = pd.read_csv("users_order.csv", encoding="utf-8")
    return render_template("users.html", users=orders_df.to_dict("records"))


@app.route("/demo-recommend")
def demo_recomm():
    """ show sample recommendation for any 1 user"""
    
    user_id = "U1001"
    bought, recommended = recommend_products(user_id)

    # Pass both purchased and recommended products to template
    return render_template(
        "recommendations.html",
        user_id=user_id,
        bought=bought,
        recommended=recommended
    )

# backend server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)