from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import current_user, login_required
from app import app, db
from models import Product, CartItem, Order, OrderItem, CategoryType, User
from auth import bp as auth_bp
import requests
import json
import uuid
from datetime import datetime
import logging

# Authentication blueprint is registered in app.py

@app.route('/')
def index():
    """Home page with featured products from all categories"""
    movies = Product.query.filter_by(category=CategoryType.MOVIE).limit(4).all()
    software = Product.query.filter_by(category=CategoryType.SOFTWARE).limit(4).all()
    games = Product.query.filter_by(category=CategoryType.GAME).limit(4).all()
    
    return render_template('index.html', 
                         movies=movies, 
                         software=software, 
                         games=games)

@app.route('/category/<category>')
def category_page(category):
    """Category page showing all products in a specific category"""
    try:
        category_enum = CategoryType(category)
    except ValueError:
        flash('Invalid category', 'error')
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'title')
    
    query = Product.query.filter_by(category=category_enum)
    
    if search:
        query = query.filter(Product.title.ilike(f'%{search}%'))
    
    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(Product.price)
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    else:
        query = query.order_by(Product.title)
    
    products = query.paginate(page=page, per_page=12, error_out=False)
    
    return render_template('category.html', 
                         products=products, 
                         category=category,
                         search=search,
                         sort_by=sort_by)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    
    # Get related products from the same category
    related_products = Product.query.filter_by(category=product.category)\
                                   .filter(Product.id != product_id)\
                                   .limit(4).all()
    
    return render_template('product_detail.html', 
                         product=product, 
                         related_products=related_products)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add product to cart"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Initialize session if needed
        if 'cart_session_id' not in session:
            session['cart_session_id'] = str(uuid.uuid4())
        
        session_id = session['cart_session_id']
        logging.debug(f"Adding product {product_id} to cart with session_id {session_id}")
        
        # Check if item already in cart
        cart_item = CartItem.query.filter_by(session_id=session_id, product_id=product_id).first()
        
        if cart_item:
            cart_item.quantity += 1
            logging.debug(f"Updated existing cart item quantity to {cart_item.quantity}")
        else:
            cart_item = CartItem()
            cart_item.session_id = session_id
            cart_item.product_id = product_id
            cart_item.quantity = 1
            db.session.add(cart_item)
            logging.debug(f"Created new cart item")
        
        db.session.commit()
        flash(f'{product.title} added to cart!', 'success')
        
        return redirect(request.referrer or url_for('index'))
    except Exception as e:
        logging.error(f"Error adding to cart: {e}")
        flash('Error adding product to cart', 'error')
        return redirect(request.referrer or url_for('index'))

@app.route('/cart')
def cart():
    """Shopping cart page"""
    if 'cart_session_id' not in session:
        cart_items = []
        total = 0
    else:
        session_id = session['cart_session_id']
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verify session ownership
    if 'cart_session_id' not in session or cart_item.session_id != session['cart_session_id']:
        flash('Invalid cart item', 'error')
        return redirect(url_for('cart'))
    
    quantity = request.form.get('quantity', type=int)
    
    if quantity and quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
        flash('Cart updated successfully!', 'success')
    else:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart!', 'success')
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verify session ownership
    if 'cart_session_id' not in session or cart_item.session_id != session['cart_session_id']:
        flash('Invalid cart item', 'error')
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart!', 'success')
    
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    """Checkout page"""
    if 'cart_session_id' not in session:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart'))
    
    session_id = session['cart_session_id']
    cart_items = CartItem.query.filter_by(session_id=session_id).all()
    
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('checkout.html', 
                         cart_items=cart_items, 
                         total=total,
                         paypal_client_id=app.config['PAYPAL_CLIENT_ID'])

@app.route('/create_paypal_order', methods=['POST'])
def create_paypal_order():
    """Create PayPal order"""
    try:
        if 'cart_session_id' not in session:
            return jsonify({'error': 'No cart found'}), 400
        
        session_id = session['cart_session_id']
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        # PayPal API endpoint
        paypal_url = "https://api.sandbox.paypal.com"
        
        # Get access token
        auth_response = requests.post(
            f"{paypal_url}/v1/oauth2/token",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en_US",
            },
            data="grant_type=client_credentials",
            auth=(app.config['PAYPAL_CLIENT_ID'], app.config['PAYPAL_CLIENT_SECRET'])
        )
        
        if auth_response.status_code != 200:
            logging.error(f"PayPal auth failed: {auth_response.text}")
            return jsonify({'error': 'PayPal authentication failed'}), 500
        
        access_token = auth_response.json()['access_token']
        
        # Create order
        order_data = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": f"{total:.2f}"
                },
                "description": "E-commerce purchase"
            }],
            "application_context": {
                "return_url": url_for('checkout_success', _external=True),
                "cancel_url": url_for('checkout', _external=True)
            }
        }
        
        order_response = requests.post(
            f"{paypal_url}/v2/checkout/orders",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            json=order_data
        )
        
        if order_response.status_code != 201:
            logging.error(f"PayPal order creation failed: {order_response.text}")
            return jsonify({'error': 'Failed to create PayPal order'}), 500
        
        order_result = order_response.json()
        
        # Store order in database
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order(
            order_number=order_number,
            session_id=session_id,
            total_amount=total,
            paypal_order_id=order_result['id'],
            status='pending'
        )
        db.session.add(order)
        db.session.commit()
        
        # Store order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        return jsonify({
            'order_id': order_result['id'],
            'order_number': order_number
        })
        
    except Exception as e:
        logging.error(f"Error creating PayPal order: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/capture_paypal_order', methods=['POST'])
def capture_paypal_order():
    """Capture PayPal order after approval"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        
        if not order_id:
            return jsonify({'error': 'Order ID required'}), 400
        
        # Find order in database
        order = Order.query.filter_by(paypal_order_id=order_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # PayPal API endpoint
        paypal_url = "https://api.sandbox.paypal.com"
        
        # Get access token
        auth_response = requests.post(
            f"{paypal_url}/v1/oauth2/token",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en_US",
            },
            data="grant_type=client_credentials",
            auth=(app.config['PAYPAL_CLIENT_ID'], app.config['PAYPAL_CLIENT_SECRET'])
        )
        
        if auth_response.status_code != 200:
            return jsonify({'error': 'PayPal authentication failed'}), 500
        
        access_token = auth_response.json()['access_token']
        
        # Capture order
        capture_response = requests.post(
            f"{paypal_url}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
        )
        
        if capture_response.status_code != 201:
            logging.error(f"PayPal capture failed: {capture_response.text}")
            return jsonify({'error': 'Failed to capture payment'}), 500
        
        # Update order status
        order.status = 'completed'
        db.session.commit()
        
        # Clear cart
        if 'cart_session_id' in session:
            CartItem.query.filter_by(session_id=session['cart_session_id']).delete()
            db.session.commit()
        
        return jsonify({
            'success': True,
            'order_number': order.order_number
        })
        
    except Exception as e:
        logging.error(f"Error capturing PayPal order: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/checkout/success')
def checkout_success():
    """Checkout success page"""
    order_number = request.args.get('order_number')
    return render_template('checkout_success.html', order_number=order_number)

@app.route('/search')
def search():
    """Search products across all categories"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    if not query:
        flash('Please enter a search term', 'error')
        return redirect(url_for('index'))
    
    search_query = Product.query.filter(Product.title.ilike(f'%{query}%'))
    
    if category:
        try:
            category_enum = CategoryType(category)
            search_query = search_query.filter_by(category=category_enum)
        except ValueError:
            pass
    
    products = search_query.all()
    
    return render_template('category.html', 
                         products=type('obj', (object,), {'items': products, 'pages': 1, 'page': 1}),
                         category='search',
                         search=query)

@app.context_processor
def utility_processor():
    """Add utility functions to template context"""
    def get_cart_count():
        if 'cart_session_id' not in session:
            return 0
        
        session_id = session['cart_session_id']
        return CartItem.query.filter_by(session_id=session_id).count()
    
    return dict(get_cart_count=get_cart_count)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
