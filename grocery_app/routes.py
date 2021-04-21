from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
)
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryItemForm, GroceryStoreForm

# Import app and db from events_app package so that we can run app
from grocery_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route("/")
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template("home.html", all_stores=all_stores)


@main.route("/new_store", methods=["GET", "POST"])
def new_store():
    # - Instantiate our grocery store form
    form = GroceryStoreForm()

    if form.validate_on_submit():
        # - Create a new grocery store object
        new_store = GroceryStore(
            title=form.title.data, address=form.address.data
        )
        db.session.add(new_store)
        db.session.commit()
        # - flash a success message, and
        flash("New store was added successfully.")
        # - redirect the user to the store detail page.
        return redirect(url_for("main.store_detail", store_id=new_store.id))
    return render_template("new_store.html", form=form)


@main.route("/new_item", methods=["GET", "POST"])
def new_item():
    form = GroceryItemForm()

    # If form was submitted and was valid:
    if form.validate_on_submit():
        # - create a new GroceryItem object and save it to the database,
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store_id=form.store.data.id,
        )
        db.session.add(new_item)
        db.session.commit()
        # - flash a success message, and
        flash("New item added successfully")
        # - redirect the user to the item detail page.
        return redirect(url_for("main.item_detail", item_id=new_item.id))
    # Send the form to the template and use it to render the form fields
    return render_template("new_item.html", form=form)


@main.route("/store/<store_id>", methods=["GET", "POST"])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)

    # If form was submitted and was valid:
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        # - update the GroceryStore object and save it to the database,
        db.session.commit()
        # - flash a success message, and
        flash("Store updated successfully")
        # - redirect the user to the store detail page.
        return redirect(url_for("main.store_detail", store_id=store.id))
    # Send the form to the template and use it to render the form fields
    store = GroceryStore.query.get(store_id)
    return render_template("store_detail.html", store=store, form=form)


@main.route("/item/<item_id>", methods=["GET", "POST"])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)
    # If form was submitted and was valid:
    if form.validate_on_submit():
        # - update the GroceryItem object and save it to the database,
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store_id = form.store.data.id

        db.session.commit()
        # - flash a success message, and
        flash("Item updated successfully!")
        # - redirect the user to the item detail page.
        return redirect(url_for("main.item_detail", item_id=item.id))
    # Send the form to the template and use it to render the form fields
    item = GroceryItem.query.get(item_id)
    return render_template("item_detail.html", item=item, form=form)
