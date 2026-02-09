import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load datasets
orders = pd.read_csv("users_order.csv")
products = pd.read_csv("all_products.csv")

# Vectorize product categories + brands for richer similarity -> string to matrix easy to compute
vectorizer = CountVectorizer()
product_vectors = vectorizer.fit_transform(
    products["product_category"] + " " + products["brand"]
)



def recommend_products(customer_id, top_n=5):

    # Get user purchase history
    user_orders = orders[orders["customer_id"] == customer_id]
    if user_orders.empty:
        return [], []
    

# Build user interest profile (categories + brands)
# If brand column exists after merging with products
    if "brand" in user_orders.columns:
      user_interest_text = " ".join(
        user_orders["product_category"].astype(str).tolist() + user_orders["brand"].dropna().astype(str).tolist()
      )
    else:
      user_interest_text = " ".join(user_orders["product_category"].astype(str).tolist())    
    
    user_vector = vectorizer.transform([user_interest_text])

#--------------

    # Compute similarity -> 0 to 1 where 1 matches
    similarity_scores = cosine_similarity(user_vector, product_vectors).flatten()

    # Attach similarity scores
    products_with_scores = products.copy()
    products_with_scores["similarity_score"] = similarity_scores

#--------------

    # Remove already purchased :-
    bought_products = user_orders["product_id"].unique()
    #-Example: If user U1001 bought P101 and 2x[P102], then bought_products = ["P101", "P102"]. uniquie already bought products by user

    recommendations = products_with_scores[~products_with_scores["product_id"].isin(bought_products)]
    #- Example: If catalog has P101, P102, P201, P301, and user already bought P101, P102, 
    # then after filtering you’ll only keep P201, P301

#--------------

    # Add hybrid scoring
    recommendations["popularity_score"] = recommendations["rating"] / 5 + (recommendations["reviews_count"] / 5000)
    recommendations["discount_score"] = (recommendations["price"] - recommendations["discount_price"]) / recommendations["price"]
    recommendations["final_score"] = (
        0.5 * recommendations["similarity_score"] +
        0.2 * recommendations["popularity_score"] +
        0.2 * recommendations["discount_score"] +
        0.1 * np.random.rand(len(recommendations))  # small diversity factor
    )

    # Sort by final score
    recommendations = recommendations.sort_values(by="final_score", ascending=False).head(top_n)

    return (
        user_orders[["product_id",
                     "product_name",
                     "product_category",
                     "quantity","price_usd",
                     "total_amount","order_date"]].to_dict("records"),
        recommendations.to_dict("records")
    )