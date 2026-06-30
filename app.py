from flask import Flask, render_template, redirect, abort, request
import json

app = Flask(__name__)

app.secret_key = "premium_savings_secret"


# Load products from JSON
def load_products():
    with open("products.json", "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def home():
    
    products = load_products()

    todays_deals = sorted(
        products,
        key=lambda x: (
            x["original_price"] - x["offer_price"]
        ),
        reverse=True
    )[:8]

    return render_template(
        "index.html",
        products=products,
        todays_deals=todays_deals
    )

# ---------------- PRODUCT DETAILS ----------------
@app.route("/product/<int:product_id>")
def product(product_id):

    products = load_products()

    selected_product = None

    for p in products:
        if p["id"] == product_id:
            selected_product = p
            break

    if selected_product:
        return render_template(
            "product.html",
            product=selected_product
        )

    abort(404)


# ---------------- BUY ----------------
@app.route("/buy/<int:product_id>")
def buy(product_id):

    products = load_products()

    for p in products:
        if p["id"] == product_id:
            return redirect(p["buy_link"])

    abort(404)


# ---------------- WISHLIST ----------------
@app.route("/wishlist")
def wishlist():

    products = load_products()

    return render_template(
        "wishlist.html",
        products=products
    )


# ---------------- CATEGORY ----------------
@app.route("/category/<category_name>")
def category(category_name):

    products = load_products()

    filtered_products = []

    for product in products:
        if product["category"].lower() == category_name.lower():
            filtered_products.append(product)

    return render_template(
        "category.html",
        products=filtered_products,
        category_name=category_name
    )


# ---------------- SEARCH ----------------
@app.route("/search")
def search():

    products = load_products()      # <<< IMPORTANT

    query = request.args.get("q", "").strip().lower()

    if query == "":
        return render_template(
            "search.html",
            products=[],
            query=""
        )

    filtered_products = []

    for product in products:

        if (
            query in product["name"].lower()
            or query in product["category"].lower()
        ):
            filtered_products.append(product)

    return render_template(
        "search.html",
        products=filtered_products,
        query=query
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
