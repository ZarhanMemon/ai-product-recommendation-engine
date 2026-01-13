import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
orders = pd.read_csv("users_order.csv")
products = pd.read_csv("all_products.csv")

# Vectorize product categories (ML PART)
vectorizer = CountVectorizer()
product_category_vectors = vectorizer.fit_transform(
    products["product_category"]
)

def recommend_products(customer_id, top_n=5):
    """
    Recommend products based on user's multi-category purchase behavior
    """

    # 1️⃣ Get user purchase history
    user_orders = orders[orders["customer_id"] == customer_id]

    if user_orders.empty:
        return [], []

    # 2️⃣ Combine all categories user purchased (IMPORTANT)
    user_interest_text = " ".join(user_orders["product_category"].tolist())

    # 3️⃣ Convert user interest to vector
    user_vector = vectorizer.transform([user_interest_text])

    # 4️⃣ Compute similarity between user & all products
    similarity_scores = cosine_similarity(
        user_vector,
        product_category_vectors
    ).flatten()

    # 5️⃣ Attach similarity scores
    products_with_scores = products.copy()
    products_with_scores["similarity_score"] = similarity_scores

    # 6️⃣ Remove already purchased products
    bought_products = user_orders["product_id"].unique()
    recommendations = products_with_scores[
        ~products_with_scores["product_id"].isin(bought_products)
    ]

    # 7️⃣ Sort by similarity_score + availability
    recommendations = recommendations.sort_values(
        by=["similarity_score", "stock_quantity"],
        ascending=False
    ).head(top_n)

    return (
        user_orders[
                [
        "product_id",
        "product_name",
        "product_category",
        "quantity",
        "price_usd",
        "total_amount",
        "order_date",
              ]
           ].to_dict("records"),
        recommendations.to_dict("records")
    )
