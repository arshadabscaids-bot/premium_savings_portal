from flask import Flask, render_template, redirect, abort, request, session 
import json

app = Flask(__name__)

app.secret_key = "premium_savings_secret"


# Load products from JSON file
def load_products():
    with open('products.json', 'r', encoding='utf-8') as file:
        return json.load(file)


# Home Page
@app.route('/')
def home():
    products = load_products()
    return render_template('index.html', products=products)


# Product Details Page
@app.route('/product/<int:product_id>')
def product(product_id):
    products = load_products()

    selected_product = None

    for p in products:
        if p['id'] == product_id:
            selected_product = p
            break

    if selected_product:
        return render_template(
            'product.html',
            product=selected_product
        )

    abort(404)


# Buy Now Redirect
@app.route('/buy/<int:product_id>')
def buy(product_id):
    products = load_products()

    for p in products:
        if p['id'] == product_id:
            return redirect(p['buy_link'])

    abort(404)


# Category Page
@app.route('/category/<category_name>')
def category(category_name):

    products = load_products()

    filtered_products = [
        product for product in products
        if product['category'].lower() == category_name.lower()
    ]

    return render_template(
        'category.html',
        products=filtered_products,
        category_name=category_name
    )

# Run Flask App
if __name__ == '__main__':
    app.run()
