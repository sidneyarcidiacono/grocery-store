"""Main routes."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.main.forms import GroceryStoreForm, GroceryItemForm
from grocery_app import app, db

main = Blueprint("main", __name__)


@main.route("/")
def homepage():
    all_stores = GroceryStore.query.all()
    return render_template("home.html", all_stores=all_stores)


@login_required
@main.route("/new_store", methods=["GET", "POST"])
def new_store():
    form = GroceryStoreForm()
    if form.validate_on_submit():
        store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user,
        )
        db.session.add(store)
        db.session.commit()
        flash("A new grocery store has been successfully created.")
        redirect(url_for("main.store_detail", store_id=store.id))
    return render_template("new_store.html", form=form)


@login_required
@main.route("/new_item", methods=["GET", "POST"])
def new_item():
    form = GroceryItemForm()
    if form.validate_on_submit():
        item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=current_user,
        )
        db.session.add(item)
        db.session.commit()
        flash("A new grocery item has been successfully created.")
        redirect(url_for("main.item_detail", item_id=item.id))
    return render_template("new_item.html", form=form)


@login_required
@main.route("/store/<store_id>", methods=["GET", "POST"])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.commit()
        flash("Grocery store has been successfully updated.")
        redirect(url_for("main.store_detail", store_id=store.id))
    return render_template("store_detail.html", store=store, form=form)


@login_required
@main.route("/item/<item_id>", methods=["GET", "POST"])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        db.session.commit()
        flash("Grocery item has been successfully updated.")
        redirect(url_for("main.item_detail", item_id=item.id))
    return render_template("item_detail.html", item=item, form=form)


@main.route("/add_to_shopping_list/<item_id>", methods=["POST"])
def add_to_shopping_list(item_id):
    """Add item to current_user's shopping list."""
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_items.append(item)
    db.session.commit()
    flash("Grocery item has been added to your shopping list.")
    redirect(url_for("main.item_detail", item_id=item_id))


@main.route("/remove_from_shopping_list/<item_id>", methods=["POST"])
@login_required
def remove_from_shopping_list(item_id):
    """Remove item from current_user's shopping list."""
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_items.remove(item)
    db.session.commit()
    flash("Grocery item has been removed from your shopping list.")
    return redirect(url_for(main.shopping_list))


@main.route("/shopping_list")
@login_required
def shopping_list():
    """Get logged in user's shopping list items."""
    return render_template("shopping_list.html")
