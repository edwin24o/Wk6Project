from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Deadly245!@localhost/ecommerce_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    accounts = db.relationship('CustomerAccount', backref='customer', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)

class CustomerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    orders = db.relationship('OrderItem', backref='product', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    try:
        new_customer = Customer(name=data['name'], email=data['email'], phone_number=data['phone_number'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer created', 'id': new_customer.id}), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/customers/<int:id>', methods=['GET'])
def read_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone_number': customer.phone_number
    })

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = Customer.query.get_or_404(id)
    try:
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone_number = data.get('phone_number', customer.phone_number)
        db.session.commit()
        return jsonify({'message': 'Customer updated'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/customer_accounts', methods=['POST'])
def create_customer_account():
    data = request.get_json()
    try:
        hashed_password = generate_password_hash(data['password'])
        new_account = CustomerAccount(username=data['username'], password=hashed_password, customer_id=data['customer_id'])
        db.session.add(new_account)
        db.session.commit()
        return jsonify({'message': 'Customer account created', 'id': new_account.id}), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/customer_accounts/<int:id>', methods=['GET'])
def read_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    return jsonify({
        'id': account.id,
        'username': account.username,
        'customer_id': account.customer_id
    })

@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    data = request.get_json()
    account = CustomerAccount.query.get_or_404(id)
    try:
        if 'username' in data:
            account.username = data['username']
        if 'password' in data:
            account.password = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify({'message': 'Customer account updated'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    try:
        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Customer account deleted'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    try:
        new_product = Product(name=data['name'], price=data['price'], stock=data.get('stock', 0))
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created', 'id': new_product.id}), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/products/<int:id>', methods=['GET'])
def read_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'stock': product.stock
    })

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    try:
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        db.session.commit()
        return jsonify({'message': 'Product updated'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'stock': p.stock
    } for p in products])

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    try:
        new_order = Order(customer_id=data['customer_id'], date=datetime.utcnow())
        db.session.add(new_order)
        for item in data['products']:
            order_item = OrderItem(order_id=new_order.id, product_id=item['product_id'], quantity=item['quantity'])
            db.session.add(order_item)
        db.session.commit()
        return jsonify({'message': 'Order placed', 'id': new_order.id}), 201
    except SQLAlchemyError as e:
        db.session.rollback() 
        return jsonify({'error': str(e)}), 400


@app.route('/orders/<int:id>', methods=['GET'])
def retrieve_order(id):
    order = Order.query.get_or_404(id)
    items = [{'product_id': i.product_id, 'quantity': i.quantity} for i in order.items]
    return jsonify({
        'id': order.id,
        'customer_id': order.customer_id,
        'date': order.date.isoformat(),
        'items': items
    })

@app.route('/orders/<int:id>/status', methods=['GET'])
def track_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({'status': 'Order status placeholder'})  

@app.route('/customers/<int:id>/orders', methods=['GET'])
def manage_order_history(id):
    customer = Customer.query.get_or_404(id)
    orders = Order.query.filter_by(customer_id=id).all()
    return jsonify([{
        'id': o.id,
        'date': o.date.isoformat(),
        'items': [{'product_id': i.product_id, 'quantity': i.quantity} for i in o.items]
    } for o in orders])

@app.route('/orders/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    order = Order.query.get_or_404(id)
    try:
        return jsonify({'message': 'Order canceled'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/orders/<int:id>/total_price', methods=['GET'])
def calculate_order_total(id):
    order = Order.query.get_or_404(id)
    total_price = sum(item.product.price * item.quantity for item in order.items)
    return jsonify({'total_price': total_price})

if __name__ == '__main__':
    app.run(debug=True)
