from flask import Flask, render_template, request, redirect, url_for, session
from recommender import recommend_products
import pandas as pd
import os

 
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session

# Initialize cart
@app.before_request
def init_cart():
    if "cart" not in session:
        session["cart"] = []


 
# ==============================
# Load Data (Only Once)
# ==============================

orders_df = pd.read_csv("users_order.csv", encoding="utf-8")
products_df = pd.read_csv("all_products.csv", encoding="utf-8")

all_products = products_df.to_dict("records")

# Demo user (simulates logged-in user)
DEMO_USER = "U1001"


# ==============================
# Home Page (Main E-commerce Page)
# ==============================

@app.route("/")
def home():
    user_id = "U1001"

    # Get search query
    query = request.args.get("search")

    # Load products
    if query:
        filtered_products = products_df[
            products_df["product_name"].str.contains(query, case=False, na=False) |
            products_df["product_category"].str.contains(query, case=False, na=False)
        ]
    else:
        filtered_products = products_df

    bought, recommended = recommend_products(user_id)

    return render_template(
        "index.html",
        recommended=recommended,
        bought=bought,
        products=filtered_products.to_dict("records"),
        search_query=query
    )


# ==============================
# Cart Feature
# ==============================

@app.route("/add_to_cart/<product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", [])
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += 1
            break
    else:
        cart.append({"product_id": product_id, "quantity": 1})
    session["cart"] = cart
    return redirect(url_for("view_cart"))



@app.route("/increase_quantity/<product_id>")
def increase_quantity(product_id):
    cart = session.get("cart", [])
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += 1
            break
    session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.route("/decrease_quantity/<product_id>")
def decrease_quantity(product_id):
    cart = session.get("cart", [])
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] -= 1
            if item["quantity"] <= 0:
                cart.remove(item)
            break
    session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.route("/remove_from_cart/<product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["product_id"] != product_id]
    session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route("/cart")
def view_cart():
    cart_items = []
    total = 0
    for item in session.get("cart", []):
        product = next((p for p in all_products if p["product_id"] == item["product_id"]), None)
        if product:
            product_copy = product.copy()
            product_copy["quantity"] = item["quantity"]
            cart_items.append(product_copy)
            # Add to total
            total += float(product["discount_price"]) * item["quantity"]
    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/reset_cart")
def reset_cart():
    session["cart"] = []
    return "Cart reset!"

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