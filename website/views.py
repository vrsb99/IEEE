from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from . import db
from .models import User, Stores, Categories, Products
views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def homepage():
    store = Stores.query.filter_by(user_id=current_user.id).first()
    categories = Categories.query.filter_by(user_id=current_user.id).all()
    store_name = store.name if store else None
    store_location = store.location if store else None
    
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
            
    
            
    if store_name and store_location and categories:
        return render_template("homepage.html", user=current_user, store_name=store_name, store_location=store_location, categories=categories)
    elif store_name and store_location:
        return render_template("homepage.html", user=current_user, store_name=store_name, store_location=store_location)
    else:
        return render_template("homepage.html", user=current_user)

@views.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_categories():
    if request.method == 'POST':
        data = request.form
        add_category = data.get('add_category')
        if add_category:
            new_category = Categories(name=add_category, user_id=current_user.id)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully', category='success')
            return redirect(url_for('views.homepage'))
        
    return render_template("add_category.html", user=current_user)


@views.route('/category/<int:category_id>', methods=['GET', 'POST'])
def items(category_id):
    category = Categories.query.filter_by(id=category_id).first() 
    items = Products.query.filter_by(category_id=category_id).all()
    
    return render_template("items.html", user=current_user, category=category, items=items)

@views.route('/add_item/<int:category_id>', methods=['GET', 'POST'])
@login_required
def add_items(category_id):
    if request.method == 'POST':
        data = request.form
        item_name = data.get('item_name')
        item_description = data.get('item_description')
        item_price = data.get('item_price')
        
        if item_name and item_price and item_description:
            new_item = Products(name=item_name, description=item_description, price=item_price, user_id=current_user.id, category_id=category_id)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully', category='success')
            return redirect(url_for('views.items', category_id=category_id))
    
    
    return render_template("add_item.html", user=current_user)