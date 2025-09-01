from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from .database import SessionLocal
from .models import Fruit, CartItem, Order, OrderItem

main = Blueprint("main", __name__)

def get_db():
    return SessionLocal()

# ------------------- API ROUTES -------------------

@main.route("/fruit", methods=["GET"])
def get_fruits():
    db = get_db()
    fruits = db.query(Fruit).all()
    return jsonify([{"id": f.id, "name": f.name, "price": f.price} for f in fruits])

@main.route("/cart", methods=["POST"])
def add_cart_item():
    db = get_db()
    data = request.get_json()
    fruit_id = data.get("fruit_id")
    quantity = data.get("quantity", 1)

    fruit = db.query(Fruit).get(fruit_id)
    if not fruit:
        return jsonify({"error": "Fruit not found"}), 404

    cart_item = db.query(CartItem).filter(CartItem.fruit_id==fruit_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(fruit_id=fruit_id, quantity=quantity)
        db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return jsonify({
        "id": cart_item.id,
        "fruit_id": cart_item.fruit_id,
        "quantity": cart_item.quantity
    }), 201

@main.route("/cart", methods=["GET"])
def view_cart():
    db = get_db()
    cart_items = db.query(CartItem).all()
    output = [{
        "id": item.id,
        "fruit": item.fruit.name,
        "quantity": item.quantity,
        "total": item.quantity * item.fruit.price
    } for item in cart_items]
    return jsonify(output)

@main.route("/cart/<int:item_id>", methods=["PUT"])
def update_cart_item(item_id):
    db = get_db()
    data = request.get_json()
    item = db.query(CartItem).get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    item.quantity = data.get("quantity", item.quantity)
    db.commit()
    return jsonify({"message": "Cart item updated"})

@main.route("/cart/<int:item_id>", methods=["DELETE"])
def delete_cart_item(item_id):
    db = get_db()
    item = db.query(CartItem).get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    db.delete(item)
    db.commit()
    return jsonify({"message": "Item deleted successfully"}), 200

@main.route("/orders", methods=["POST"])
def place_order():
    db = get_db()
    cart_items = db.query(CartItem).all()
    if not cart_items:
        return jsonify({"error": "Your cart is empty"}), 400

    order = Order(status="Pending")
    db.add(order)
    db.commit()
    db.refresh(order)

    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            fruit_id=cart_item.fruit_id,
            quantity=cart_item.quantity,
            price=cart_item.fruit.price
        )
        db.add(order_item)
        db.delete(cart_item)

    db.commit()
    return jsonify({"message": "Order placed successfully", "order_id": order.id, "status": order.status}), 201

@main.route("/orders", methods=["GET"])
def get_orders():
    db = get_db()
    orders = db.query(Order).all()
    output = []
    for order in orders:
        items = [{
            "fruit_id": item.fruit_id,
            "quantity": item.quantity,
            "price": item.fruit.price
        } for item in order.items]

        output.append({
            "id": order.id,
            "status": order.status,
            "created_at": order.created_at,
            "items": items
        })
    return jsonify(output)

# ------------------- FRONTEND ROUTES -------------------

@main.route("/")
def index():
    db = get_db()
    fruits = db.query(Fruit).all()
    return render_template("index.html", fruits=fruits)

@main.route("/add-fruit", methods=["GET", "POST"])
def add_fruit():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description")
        price = request.form.get("price")

        existing = db.query(Fruit).filter(Fruit.name.ilike(name)).first()
        if existing:
            flash(f"Fruit '{name}' already exists!", "danger")
            return redirect(url_for("main.add_fruit"))

        new_fruit = Fruit(name=name, description=description, price=float(price))
        db.add(new_fruit)
        db.commit()
        flash(f"Fruit '{name}' added successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("add_fruit.html")

@main.route("/add-to-cart/<int:fruit_id>", methods=["POST"])
def add_to_cart(fruit_id):
    db = get_db()
    quantity = int(request.form.get("quantity", 1))
    fruit = db.query(Fruit).get(fruit_id)
    if not fruit:
        flash("Fruit not found!", "danger")
        return redirect(url_for("main.index"))

    cart_item = db.query(CartItem).filter(CartItem.fruit_id==fruit_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(fruit_id=fruit_id, quantity=quantity)
        db.add(cart_item)
    db.commit()
    return redirect(url_for("main.view_cart_page"))

@main.route("/cart-page")
def view_cart_page():
    db = get_db()
    cart_items = db.query(CartItem).all()
    total = sum(item.quantity * item.fruit.price for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total=total)
