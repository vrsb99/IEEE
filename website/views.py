from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import login_required, current_user
from . import db
from .models import User, Stores, Categories, Products, Orders, Customers
views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def original():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')
    
    return render_template("login.html", user=current_user)

@views.route('/homepage', methods=['GET','POST'])
@login_required
def homepage():
    store = Stores.query.filter_by(user_id=current_user.id).first()
    categories = Categories.query.filter_by(user_id=current_user.id).all()
    store_name = store.name if store else None
    store_location = store.location if store else None
    store_id = store.id if store else None
    orders = Orders.query.filter_by(store_id=store_id).all() if store_id else None
    
    total = Orders.query.filter_by(store_id=store_id).with_entities(db.func.sum(Orders.total)).scalar() if store_id else None
    
    if orders:
        order_info = []
        for order in orders:
            order_details = {}
            order_details['id'] = order.id
            order_details['customer_email'] = Customers.query.filter_by(id=order.customers_id).first().email
            order_details['product_name'] = Products.query.filter_by(id=order.products_id).first().name
            order_details['quantity'] = order.quantity
            order_details['total'] = order.quantity * Products.query.filter_by(id=order.products_id).first().price
            order_info.append(order_details)
        
    
    
    if request.method == 'POST':
        data = request.form
        store_name_input = data.get('store_name')
        store_location_input = data.get('store_location')
        
        if store_name_input and store_location_input:
            
            if store_name and store_location:
                store.name = store_name_input
                store.location = store_location_input
            else:
                new_store = Stores(name=store_name_input, location=store_location_input, user_id=current_user.id)
                db.session.add(new_store)

            db.session.commit()
            flash('Store added successfully', category='success')
            return redirect(url_for('views.homepage'))
        else:
            flash('Please fill all the fields', category='error')
            
    if store_name and store_location and categories and orders:
        return render_template("homepage.html", user=current_user, store_name=store_name, store_location=store_location, categories=categories, store_id=store_id, order_info=order_info, total=total)
    elif store and categories:
        return render_template("homepage.html", user=current_user, store_name=store_name, store_location=store_location, categories=categories, store_id=store_id)
    elif store:
        return render_template("homepage.html", user=current_user, store_name=store_name, store_location=store_location, store_id=store_id)
    else:
        return render_template("homepage.html", user=current_user)

@views.route('/add_category/<int:store_id>', methods=['GET', 'POST'])
@login_required
def add_categories(store_id):
    if request.method == 'POST':
        data = request.form
        add_category = data.get('add_category')
        if add_category:
            new_category = Categories(name=add_category, user_id=current_user.id, store_id=store_id)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully', category='success')
            return redirect(url_for('views.homepage'))
        
    return render_template("add_category.html", user=current_user)


@views.route('/category/<int:store_id>/<int:category_id>', methods=['GET', 'POST'])
def items(store_id, category_id):
    category = Categories.query.filter_by(id=category_id).first()
    items = Products.query.filter_by(category_id=category_id).all()
    
    return render_template("items.html", user=current_user, category=category, items=items, store_id=store_id)

@views.route('/add_item/<int:store_id>/<int:category_id>', methods=['GET', 'POST'])
@login_required
def add_items(store_id, category_id):
    if request.method == 'POST':
        data = request.form
        item_name = data.get('item_name')
        item_description = data.get('item_description')
        item_price = data.get('item_price')
        
        if item_name and item_price and item_description:
            new_item = Products(name=item_name, description=item_description, price=item_price, user_id=current_user.id, category_id=category_id, store_id=store_id)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully', category='success')
            return redirect(url_for('views.items', category_id=category_id, store_id=store_id))
    
    
    return render_template("add_item.html", user=current_user)

@views.route('/qr/<int:store_id>')
@login_required
def qr(store_id):
    return render_template("qr.html", user=current_user, store_id=store_id)