 
---

# 🛒 E-Commerce Product Recommendation System (Enhanced Version)

A **Flask-based product recommendation system** that analyzes user purchase history from CSV files and recommends relevant products based on **category preferences, brand affinity, discounts, popularity, and similarity scoring**.

This project is designed to be **simple, explainable, and demo-ready**, suitable for:

* Mini-project / AI-ML integration demo  
* Backend recommendation logic showcase  

---

## 📌 Problem Statement

E-commerce platforms need to recommend products that match a user's interests while also considering **brand loyalty, product popularity, and discounts**.

In this project, we:

1. Analyze **past user orders** stored in a CSV file  
2. Identify the user’s **interest patterns** (categories, brands, frequency, recency)  
3. Recommend **new products** from another CSV file  
4. Compute a **hybrid similarity score** (category + brand + popularity + discount)  
5. Display results in a **web dashboard** using Flask + Jinja2  

All data is handled **offline using CSV files** (no database required).  

---

## 🧠 How the System Works (High Level)

```
User selects Customer ID
        ↓
System reads users_order.csv
        ↓
Finds dominant categories, brands & purchase behavior
        ↓
Matches with all_products.csv
        ↓
Computes hybrid similarity score
        ↓
Displays recommendations with explainability
```

---

## 📂 Project Structure

```
project-root/
│
├── app.py                    # Flask application
├── recommender.py            # Recommendation logic (hybrid scoring)
│
├── data/
│   ├── users_order.csv       # User purchase history
│   └── all_products.csv      # Product catalog with brand, rating, reviews
│
├── templates/
│   ├── index.html            # User selection page
│   ├── recommendations.html  # Recommendation dashboard
│   ├── products.html         # Full catalog view
│   └── users.html            # All users & purchase histories
│
├── static/
│   └── images/               # Optional local images
│
└── README.md
```

---

## 📊 Dataset Description

### 1️⃣ users_order.csv (User Purchase History)

Each row represents **one product purchase** by a user.

**Columns:**

* `customer_id` – Unique user ID  
* `product_id` – Product identifier  
* `product_name` – Name of product  
* `product_category` – Category (Electronics, Fashion, etc.)  
* `quantity` – Quantity purchased  
* `price_usd` – Price per unit  
* `payment_method` – Credit Card / Debit Card / Paypal / UPI  
* `order_date` – Purchase date  
* `total_amount` – Final order value  

✔ Users can purchase **multiple categories and brands** over time  

---

### 2️⃣ all_products.csv (Product Catalog)

Contains **all available products** on the platform.

**Columns:**

* `product_id`  
* `product_name`  
* `product_category`  
* `price`  
* `discount_price`  
* `stock_quantity`  
* `image_url` (public real image URLs)  
* `brand`  
* `rating` (1–5 stars)  
* `reviews_count` (number of reviews)  

---

## 🤖 Recommendation Logic (Core Idea)

The system uses a **hybrid content-based filtering approach**:

### 🔹 Step 1: User Profiling
* Count category-wise purchases  
* Identify dominant brands & categories  
* Consider quantity and recency  

### 🔹 Step 2: Product Matching
* Recommend products from:  
  * Frequently bought categories  
  * Same brands or related brands  
* Exclude already purchased products  

### 🔹 Step 3: Hybrid Similarity Score
Each recommended product gets a score based on:

* Category match (cosine similarity)  
* Brand affinity  
* Popularity (rating + reviews)  
* Discount attractiveness  
* Recency bonus  

Example:

```
Final Score = 0.5 * Category Similarity
            + 0.2 * Popularity
            + 0.2 * Discount
            + 0.1 * Diversity Factor
```

This score is shown in the UI for **explainability**.

---

## 🖥️ Web Application Flow

1️⃣ User selects **Customer ID** from dropdown  

2️⃣ System shows:  
* Previously purchased products  
* Recommended products  

3️⃣ Recommendation cards include:  
* Product image  
* Name, category, brand  
* Price (with discount)  
* Rating & reviews  
* Similarity score badge  

---

## ⚙️ Technologies Used

* **Python 3**  
* **Flask** – Backend web framework  
* **Pandas** – Data processing  
* **Scikit-learn** – Cosine similarity  
* **Jinja2** – HTML templating  
* **Bootstrap 5** – Frontend styling  
* **CSV Files** – Data storage  

---

## ▶️ How to Run the Project

```bash
pip install flask pandas scikit-learn
python app.py
```

Then open:

```bash
http://127.0.0.1:5000/
```

---

## 🎓 Academic Value (For HOD / Faculty)

✔ Demonstrates real-world recommendation logic  
✔ Clear separation of data, logic, and UI  
✔ Explainable AI (hybrid similarity scores)  
✔ No heavy infrastructure required  
✔ Easily extensible to ML models  

---

## 🚀 Future Enhancements

* Collaborative filtering  
* ML-based embeddings (Word2Vec, BERT)  
* User clustering  
* Database integration (MySQL / MongoDB)  
* Login-based personalization  
* Chart.js analytics (category distribution, score breakdown)  

---

## 📌 Conclusion

This project simulates a **real e-commerce recommendation engine** using hybrid scoring (category + brand + popularity + discount), making it ideal for **learning, demos, and academic evaluation**.  

---

👉 Would you like me to also **add a section in the README with screenshots of the UI (recommendations.html, products.html, users.html)** so your faculty demo looks even more professional?
