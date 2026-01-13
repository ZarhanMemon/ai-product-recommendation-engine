# 🛒 CSV-Based E-Commerce Product Recommendation System

A **Flask-based product recommendation system** that analyzes user purchase history from CSV files and recommends relevant products based on category preferences, purchase behavior, and similarity scoring.

This project is designed to be **simple, explainable, and demo-ready**, suitable for:

* Academic evaluation (HOD / Faculty demo)
* Mini-project / AI-ML integration demo
* Backend recommendation logic showcase

---

## 📌 Problem Statement

E-commerce platforms need to recommend products that match a user's interests.

In this project, we:

1. Analyze **past user orders** stored in a CSV file
2. Identify the user’s **interest patterns** (categories, frequency, recency)
3. Recommend **new products** from another CSV file
4. Display results in a **web dashboard** using Flask + Jinja2

All data is handled **offline using CSV files** (no database required).

---

## 🧠 How the System Works (High Level)

```
User selects Customer ID
        ↓
System reads users_order.csv
        ↓
Finds dominant categories & purchase behavior
        ↓
Matches with products.csv
        ↓
Computes similarity score
        ↓
Displays recommendations on UI
```

---

## 📂 Project Structure

```
project-root/
│
├── app.py                    # Flask application
├── recommender.py            # Recommendation logic
│
├── data/
│   ├── users_order.csv       # User purchase history
│   └── products.csv          # Product catalog
│
├── templates/
│   ├── index.html             # User selection page
│   └── recommendations.html  # Recommendation dashboard
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
* `payment_method` – Credit Card / Debit Card / Paypal
* `order_date` – Purchase date
* `total_amount` – Final order value

✔ Users can purchase **multiple categories** over time

---

### 2️⃣ products.csv (Product Catalog)

Contains **all available products** on the platform.

**Columns:**

* `product_id`
* `product_name`
* `product_category`
* `price`
* `stock_quantity`
* `image_url` (public real image URLs)

---

## 🤖 Recommendation Logic (Core Idea)

The system uses a **content-based filtering approach**:

### 🔹 Step 1: User Profiling

* Count category-wise purchases
* Identify dominant & secondary interests
* Consider quantity and recency

### 🔹 Step 2: Product Matching

* Recommend products from:

  * Frequently bought categories
  * Related categories
* Exclude already purchased products

### 🔹 Step 3: Similarity Score

Each recommended product gets a score based on:

* Category match
* Purchase frequency
* Recency weight

Example:

```
Similarity Score = Category Match Weight + Frequency Weight + Recency Bonus
```

This score is shown in the UI for **explainability**.

---

## 🖥️ Web Application Flow

1️⃣ User selects **Customer ID** from dropdown

2️⃣ System shows:

* Previously purchased products
* Recommended products

3️⃣ Recommendation table includes:

* Product image
* Name & category
* Price
* Similarity score

---

## ⚙️ Technologies Used

* **Python 3**
* **Flask** – Backend web framework
* **Pandas** – Data processing
* **Jinja2** – HTML templating
* **CSV Files** – Data storage

---

## ▶️ How to Run the Project

```bash
pip install flask pandas
python app.py
```

Then open:

```
http://127.0.0.1:5000/
```

---

## 🎓 Academic Value (For HOD / Faculty)

✔ Demonstrates real-world recommendation logic
✔ Clear separation of data, logic, and UI
✔ Explainable AI (similarity scores)
✔ No heavy infrastructure required
✔ Easily extensible to ML models

---

## 🚀 Future Enhancements

* Collaborative filtering
* ML-based similarity (cosine similarity)
* User clustering
* Database integration (MySQL / MongoDB)
* Login-based personalization

---

## 👨‍💻 Team Notes

* Dataset can be expanded easily
* Recommendation logic is modular
* UI is fully customizable

---

## 📌 Conclusion

This project simulates a **real e-commerce recommendation engine** using simple yet powerful techniques, making it ideal for learning, demos, and academic evaluation.

---

📢 *For any clarification or enhancement requests, refer to `recommender.py` for core logic.*
