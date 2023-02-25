from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from . import db
from .models import Stores, Categories, Products

menu = Blueprint('menu', __name__)

@menu.route('/<int:store_id>', methods=['GET', 'POST'])
def homepage(store_id):
    store = Stores.query.filter_by(id=store_id).first()
    categories = Categories.query.filter_by(store_id=store_id).all()
    products = Products.query.filter_by(store_id=store_id).all()
    print([(product.name,product.category_id) for product in products])
    return render_template("menu.html", user=current_user, store=store, categories=categories, products=products)

