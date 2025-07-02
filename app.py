from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PRODUCTS_FILE'] = 'products.json'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load or initialize products
if not os.path.exists(app.config['PRODUCTS_FILE']):
    with open(app.config['PRODUCTS_FILE'], 'w') as f:
        json.dump([], f)

def load_products():
    with open(app.config['PRODUCTS_FILE'], 'r') as f:
        return json.load(f)

def save_product(product):
    products = load_products()
    products.append(product)
    with open(app.config['PRODUCTS_FILE'], 'w') as f:
        json.dump(products, f, indent=4)

@app.route('/')
def index():
    products = load_products()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        image_file = request.files['image']

        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_url = os.path.join('uploads', filename)
        else:
            image_url = ''

        product = {
            'name': name,
            'category': category,
            'description': description,
            'image': image_url
        }
        save_product(product)
        return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/products/<category>')
def products_by_category(category):
    category = category.lower()
    products = load_products()
    filtered = [p for p in products if p['category'].lower() == category]
    return render_template('category.html', products=filtered, category=category.capitalize())

@app.route('/api/products')
def get_products():
    return jsonify(load_products())

if __name__ == '__main__':
    app.run(debug=True)
