from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Stores, Categories, Products, Orders
import base64

menu = Blueprint("menu", __name__)


@menu.route("/<int:store_id>", methods=["GET", "POST"])
def homepage(store_id):
    store = Stores.query.filter_by(id=store_id).first()
    categories = Categories.query.filter_by(store_id=store_id).all()
    products = Products.query.filter_by(store_id=store_id).all()
    images = {}

    if not store:
        return redirect(url_for("views.homepage"))

    for product in products:
        if product.image:
            images[product.id] = base64.b64encode(product.image).decode("utf-8")

    # Post for orders table
    if request.method == "POST":
        data = request.form

        for product in products:
            if value := data.get(str(product.id)):
                new_order = Orders(
                    products_id=product.id, quantity=int(value), store_id=store_id
                )
                new_order.total = new_order.quantity * product.price
                db.session.add(new_order)
                db.session.commit()
                flash("Order added successfully", category="success")

        return redirect(url_for("menu.homepage", store_id=store_id))

    return render_template(
        "menu.html",
        store=store,
        categories=categories,
        products=products,
        images=images,
    )
