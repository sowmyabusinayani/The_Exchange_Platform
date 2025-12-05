from flask import jsonify, Flask, request, render_template
from models.flower import Flower
from models.customer import Customer
from models.order import Order

app = Flask(__name__)

flowers = {
    "Orchid": Flower("Orchid", 20, 100),
    "Tulip": Flower("Tulip", 30, 100)
}

customers = {
    9: Customer(9, "arya"),
    8: Customer(8, "puja")
}

orders = {}
next_order_id = 1


@app.route("/")
def home():
    # Return the HTML page with our JS frontend
    return render_template("index.html")


@app.route("/flowers", methods=['GET'])
def get_flowers():
    data = [flower.to_dict() for flower in flowers.values()]
    return jsonify(data), 200


@app.route("/customers", methods=['GET'])
def get_customers():
    data = [customer.to_dict() for customer in customers.values()]
    return jsonify(data), 200


@app.route("/orders", methods=['POST'])
def create_order():
    global next_order_id
    body = request.get_json()

    # checking whether body is empty or not to avoid internal server error
    if not body:
        return jsonify({"error:Invalid JSON body"}, 400)

    # Extracts required values from incoming JSON
    customer_id = body.get("customer_id")
    flower_name = body.get("flower_name")
    quantity = body.get("quantity")

    if customer_id not in customers:
        return jsonify({"error: customer not found"}, 404)

    if flower_name not in flowers:
        return jsonify({"error: flower not found"}, 404)

    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"error: Quantity must be positive integer"}, 400)

    customer = customers[customer_id]
    flower = flowers[flower_name]

    # Creates Order object
    order = Order(next_order_id, customer, flower, quantity)

    # Applies business logic: validate stock, update stock, set status
    order.place_order()

    # Saves the new order in our "database"
    orders[next_order_id] = order

    next_order_id += 1

    # Returns newly created order in JSON
    return jsonify(order.to_dict()), 201


 # Runs the Flask server only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
