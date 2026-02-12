from flask import Flask, render_template, request, jsonify, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Product Database
products_db = {
    "fruits": [
        {"id": 1, "name": "Apple", "price": 120, "category": "fruits", "image": "🍎"},
        {"id": 2, "name": "Banana", "price": 40, "category": "fruits", "image": "🍌"},
        {"id": 3, "name": "Orange", "price": 60, "category": "fruits", "image": "🍊"},
        {"id": 4, "name": "Mango", "price": 150, "category": "fruits", "image": "🥭"},
        {"id": 5, "name": "Grapes", "price": 90, "category": "fruits", "image": "🍇"},
        {"id": 6, "name": "Pineapple", "price": 70, "category": "fruits", "image": "🍍"},
        {"id": 7, "name": "Papaya", "price": 50, "category": "fruits", "image": "🧡"},
        {"id": 8, "name": "Watermelon", "price": 30, "category": "fruits", "image": "🍉"},
        {"id": 9, "name": "Kiwi", "price": 180, "category": "fruits", "image": "🥝"},
        {"id": 10, "name": "Strawberry", "price": 200, "category": "fruits", "image": "🍓"},
        {"id": 11, "name": "Cherry", "price": 250, "category": "fruits", "image": "🍒"},
        {"id": 12, "name": "Peach", "price": 160, "category": "fruits", "image": "🍑"},
        {"id": 13, "name": "Pear", "price": 110, "category": "fruits", "image": "🍐"},
        {"id": 14, "name": "Lemon", "price": 35, "category": "fruits", "image": "🍋"},
        {"id": 15, "name": "Pomegranate", "price": 170, "category": "fruits", "image": "🔴"},
        {"id": 16, "name": "Coconut", "price": 45, "category": "fruits", "image": "🥥"},
        {"id": 17, "name": "Guava", "price": 60, "category": "fruits", "image": "🍏"},
        {"id": 18, "name": "Lychee", "price": 220, "category": "fruits", "image": "🍒"},
        {"id": 19, "name": "Blueberry", "price": 300, "category": "fruits", "image": "🫐"},
        {"id": 20, "name": "Avocado", "price": 240, "category": "fruits", "image": "🥑"}


    ],
  "vegetables": [
    {"id": 21, "name": "Potato", "price": 40, "category": "vegetables", "image": "🥔"},
    {"id": 22, "name": "Onion", "price": 45, "category": "vegetables", "image": "🧅"},
    {"id": 23, "name": "Tomato", "price": 50, "category": "vegetables", "image": "🍅"},
    {"id": 24, "name": "Carrot", "price": 55, "category": "vegetables", "image": "🥕"},
    {"id": 25, "name": "Cabbage", "price": 35, "category": "vegetables", "image": "🥬"},
    {"id": 26, "name": "Cauliflower", "price": 60, "category": "vegetables", "image": "🥦"},
    {"id": 27, "name": "Spinach", "price": 30, "category": "vegetables", "image": "🌿"},
    {"id": 28, "name": "Peas", "price": 70, "category": "vegetables", "image": "💚"},
    {"id": 29, "name": "Brinjal", "price": 50, "category": "vegetables", "image": "🍆"},
    {"id": 30, "name": "Capsicum", "price": 65, "category": "vegetables", "image": "🫑"}
  ],

  "shoes": [
    {"id": 31, "name": "Sports Shoes", "price": 2510, "category": "shoes", "image": "👟"},
    {"id": 32, "name": "Running Shoes", "price": 2210, "category": "shoes", "image": "👞"},
    {"id": 33, "name": "Formal Shoes", "price": 3010, "category": "shoes", "image": "👞"},
    {"id": 34, "name": "Casual Shoes", "price": 1810, "category": "shoes", "image": "👟"},
    {"id": 35, "name": "Loafers", "price": 2010, "category": "shoes", "image": "👞"},
    {"id": 36, "name": "Sneakers", "price": 2710, "category": "shoes", "image": "👟"}
  ],

  "shirts": [
    {"id": 37, "name": "T-Shirt", "price": 610, "category": "shirts", "image": "👕"},
    {"id": 38, "name": "Formal Shirt", "price": 1510, "category": "shirts", "image": "👔"},
    {"id": 39, "name": "Casual Shirt", "price": 1210, "category": "shirts", "image": "👕"},
    {"id": 40, "name": "Denim Shirt", "price": 1710, "category": "shirts", "image": "👕"},
    {"id": 41, "name": "Checked Shirt", "price": 1310, "category": "shirts", "image": "👕"}
  ],

  "pants": [
    {"id": 42, "name": "Jeans", "price": 2010, "category": "pants", "image": "👖"},
    {"id": 43, "name": "Cotton Pant", "price": 1610, "category": "pants", "image": "👖"},
    {"id": 44, "name": "Formal Pant", "price": 2210, "category": "pants", "image": "👖"},
    {"id": 45, "name": "Chinos", "price": 1910, "category": "pants", "image": "👖"},
    {"id": 46, "name": "Track Pant", "price": 910, "category": "pants", "image": "👖"}
  ]


}

def get_all_products():
    """Get all products from all categories"""
    all_products = []
    for category in products_db.values():
        all_products.extend(category)
    return all_products

@app.route('/')
def index():
    """Home page with all products"""
    categories = list(products_db.keys())
    return render_template('index.html', categories=categories)

@app.route('/api/products')
def get_products():
    """Get products - filtered by category or search"""
    category = request.args.get('category', '').lower()
    search = request.args.get('search', '').lower()
    
    all_products = get_all_products()
    
    # Filter by category
    if category and category in products_db:
        filtered = products_db[category]
    else:
        filtered = all_products
    
    # Filter by search
    if search:
        filtered = [p for p in filtered if search in p['name'].lower()]
    
    return jsonify(filtered)

@app.route('/api/cart', methods=['GET', 'POST'])
def cart():
    """Manage shopping cart"""
    if 'cart' not in session:
        session['cart'] = []
    
    if request.method == 'POST':
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        # Find product
        all_products = get_all_products()
        product = next((p for p in all_products if p['id'] == product_id), None)
        
        if product:
            # Check if product already in cart
            cart_item = next((item for item in session['cart'] if item['id'] == product_id), None)
            
            if cart_item:
                cart_item['quantity'] += quantity
            else:
                session['cart'].append({
                    'id': product_id,
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': quantity,
                    'image': product['image']
                })
            
            session.modified = True
            return jsonify({'success': True, 'message': 'Added to cart'})
    
    # Calculate total
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    
    return jsonify({
        'items': session['cart'],
        'total': total,
        'count': len(session['cart'])
    })

@app.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    """Remove item from cart"""
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        session.modified = True
    
    return jsonify({'success': True})

@app.route('/api/cart/update/<int:product_id>', methods=['PUT'])
def update_cart(product_id):
    """Update cart item quantity"""
    if 'cart' in session:
        data = request.get_json()
        quantity = data.get('quantity', 1)
        
        for item in session['cart']:
            if item['id'] == product_id:
                item['quantity'] = quantity
                break
        
        session.modified = True
    
    return jsonify({'success': True})

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Process checkout/payment"""
    if 'cart' not in session or not session['cart']:
        return jsonify({'success': False, 'message': 'Cart is empty'}), 400
    
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    payment_method = data.get('payment_method')
    
    # Calculate total
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    
    # Here you would process the payment
    # For now, we'll just simulate success
    
    response = {
        'success': True,
        'message': 'Order placed successfully!',
        'order_id': 'ORD-' + str(int(session.get('last_order_id', 1000)) + 1),
        'total': total,
        'customer': name
    }
    
    session['last_order_id'] = int(session.get('last_order_id', 1000)) + 1
    session['cart'] = []
    session.modified = True
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


