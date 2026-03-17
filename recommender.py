import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load datasets
orders = pd.read_csv("users_order.csv")
products = pd.read_csv("all_products.csv")

# If orders has "price" instead of "price_usd", rename it
if "price" in orders.columns and "price_usd" not in orders.columns:
    orders = orders.rename(columns={"price": "price_usd"})

# Vectorize product categories + brands for richer similarity
vectorizer = CountVectorizer()
product_vectors = vectorizer.fit_transform(
    products["product_category"] + " " + products["brand"]
)

def recommend_products(customer_id, top_n=5):
    # Get user purchase history
    user_orders = orders[orders["customer_id"] == customer_id]
    if user_orders.empty:
        return [], []

    # Build user interest profile
    if "brand" in user_orders.columns:
        user_interest_text = " ".join(
            user_orders["product_category"].astype(str).tolist()
            + user_orders["brand"].dropna().astype(str).tolist()
        )
    else:
        user_interest_text = " ".join(user_orders["product_category"].astype(str).tolist())

    user_vector = vectorizer.transform([user_interest_text])

    # Compute similarity
    similarity_scores = cosine_similarity(user_vector, product_vectors).flatten()

    # Attach similarity scores
    products_with_scores = products.copy()
    products_with_scores["similarity_score"] = similarity_scores

    # Remove already purchased
    bought_products = user_orders["product_id"].unique()
    recommendations = products_with_scores[
        ~products_with_scores["product_id"].isin(bought_products)
    ]

    # Add hybrid scoring
    recommendations["popularity_score"] = (
        recommendations["rating"] / 5 + (recommendations["reviews_count"] / 5000)
    )
    recommendations["discount_score"] = (
        (recommendations["price"] - recommendations["discount_price"]) / recommendations["price"]
    )
    recommendations["final_score"] = (
        0.5 * recommendations["similarity_score"]
        + 0.2 * recommendations["popularity_score"]
        + 0.2 * recommendations["discount_score"]
        + 0.1 * np.random.rand(len(recommendations))  # diversity factor
    )

    # Sort by final score
    recommendations = recommendations.sort_values(by="final_score", ascending=False).head(top_n)

    return (
        user_orders[
            [
                "product_id","product_img","product_name",
                "product_category","quantity","price_usd",
                "total_amount","order_date"
            ]
        ].to_dict("records"),
        recommendations[
            [
                "product_id","image_url","product_name",
                "product_category","brand","price","discount_price",
                "discount_score","similarity_score","final_score"
            ]
        ].to_dict("records")
    )