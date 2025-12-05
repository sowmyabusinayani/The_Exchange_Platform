from flask import jsonify, Flask, request, render_template
from models.flower import Flower
from models.customer import Customer
from models.order import Order

app = Flask(__name__)

# Mock data
flowers = [
    Flower(1, "Pink Tulips", 450, 10,
           "https://images.unsplash.com/photo-1561181226-e8a7edd504c6?q=80&w=687&auto=format&fit=crop"),
    Flower(2, "White Rice Flower Bouquet", 320, 5,
           "https://plus.unsplash.com/premium_photo-1668790459193-95f86452a5dc?q=80&w=735&auto=format&fit=crop"),
    Flower(3, "Royal Red Rose", 500, 8,
           "https://plus.unsplash.com/premium_photo-1669997827506-e8e7aa33e7e3?q=80&w=687&auto=format&fit=crop"),
    Flower(4, "Sunflower Bundle", 280, 15,
           "https://plus.unsplash.com/premium_photo-1676068244464-59294c6ff008?q=80&w=1170&auto=format&fit=crop")
]

customers = [
    Customer(101, "Otani Trading HQ", "admin@otanitrading.com"),
    Customer(102, "Dubai Floral Shop", "buyer@dubaifloral.com"),
    Customer(103, "Events UAE", "manager@eventsuae.ae")
]

orders = []  # Simple list to store Order objects in memory
next_order_id = 1


@app.route("/")
def home():
    # Return the HTML page with our JS frontend
    return render_template("index.html")


@app.route("/flowers", methods=['GET'])
def get_flowers():
    # Returns list of flowers with Image URL and Stock Status
    data = [fwr.to_dict() for fwr in flowers]
    return jsonify(data), 200


@app.route("/customers", methods=['GET'])
def get_customers():
    data = [cust.to_dict() for cust in customers.values()]
    return jsonify(data), 200


@app.route('/orders', methods=['GET'])
def get_orders():
    # Returns order history for the Admin Dashboard
    data = [ord.to_dict() for ord in orders]
    return jsonify(data)


@app.route("/orders", methods=['POST'])
def create_order():
    data = request.json
    # Validation: Ensure data is a list
    if not isinstance(data, list):
        return jsonify({"error": "Invalid format. Expected a list of items."}), 400

    results = []
    # Default customer
    current_customer = customers[1]
    for item in data:
        f_id = item.get('flower_id')
        qty = item.get('quantity')
        # 1. Find the flower object
        flower = next((f for f in flowers if f.flower_id == f_id), None)

        if not flower:
            results.append({"id": f_id, "status": "Failed",
                           "reason": "Flower not found"})
            continue

        # 2. Create the Order Object
        new_order_id = len(orders) + 1
        order = Order(new_order_id, current_customer, flower, qty)

        # 3. Process the Order (Check Stock -> Commit Stock)
        success, message = order.place_order()  # Using the renamed method

        if success:
            orders.append(order)
            results.append({
                "flower": flower.name,
                "status": "Confirmed",
                "total_price": order.total_price
            })
        else:
            results.append({
                "flower": flower.name,
                "status": "Failed",
                "reason": message
            })
    return jsonify({"message": "Batch processed", "results": results})


 # Runs the Flask server only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
