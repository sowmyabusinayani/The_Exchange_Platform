from flask import jsonify, Flask, request, render_template, redirect
from models.flower import Flower
from models.customer import Customer
from models.order import Order
from models.url_shortner import URLShortener

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

url_shortener = URLShortener()

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
    #  Returns basic order list.
    data = [ord.to_dict() for ord in orders]
    return jsonify(data)


@app.route("/orders", methods=['POST'])
def create_order():
    global next_order_id
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
            results.append({"id": f_id,
                            "status": "Failed",
                            "reason": "Flower not found"})
            continue

        # 2. Create the Order Object
        new_order_id = len(orders) + 1
        order = Order(new_order_id, current_customer, flower, qty)

        # 3. Process the Order (Check Stock -> Commit Stock)
        success, message = order.place_order()  # Using the renamed method

        if success:
            orders.append(order)
            # Creating a tracking link
            tracking_url = f"{request.host_url}orders/details/{order.order_id}"

            # Generate short URL for sharing
            short_code = url_shortener.shorten(
                tracking_url, purpose="order_tracking")
            short_url = f"{request.host_url}t/{short_code}"

            results.append({
                "order_id": order.order_id,
                "flower": flower.name,
                "quantity": qty,
                "status": "Confirmed",
                "total_price": order.total_price,
                "tracking_url": tracking_url,
                "share_link": short_url
            })
        else:
            results.append({
                "flower": flower.name,
                "status": "Failed",
                "reason": message
            })
    return jsonify({"message": "Batch processed", "results": results})

    # NEW: Get All Orders (For "My Orders" page)


@app.route('/my-orders', methods=['GET'])
def get_my_orders():
    if not orders:
        return jsonify({
            "orders": [],
            "message": "No orders placed yet"
        }), 200
    order_list = []
    for order in orders:
        tracking_url = f"{request.host_url}orders/details/{order.order_id}"
        short_code = url_shortener.shorten(
            tracking_url, purpose="order_tracking")
        short_url = f"{request.host_url}t/{short_code}"
        order_list.append({
            "order_id": order.order_id,
            "flower_name": order.flower.name,
            "flower_image": order.flower.image_url,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "status": order.status,
            "date": order.timestamp.strftime("%b %d, %Y %H:%M"),
            "tracking_url": tracking_url,
            "share_link": short_url
        })
    return jsonify({
        "orders": order_list,
        "count": len(order_list)
    }), 200

    # Get Order Details (For detailed tracking page)


@app.route('/orders/details/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    """
    Returns detailed information for a specific order.

        This page is accessible via:
        1. Direct URL: /orders/details/10492
        2. Short URL: /t/aB3xK9 (redirects here)
         - Complete order information
         - Customer details
         - Flower details with image
         - Shareable short link
    """
    order = next((o for o in orders if o.order_id == order_id), None)
    if not order:
        return jsonify({
            "error": "Order not found",
            "message": f"No order exists with ID {order_id}"
        }), 404
     # Generate shareable link
    tracking_url = f"{request.host_url}orders/details/{order.order_id}"
    short_code = url_shortener.shorten(
        tracking_url, purpose="order_tracking")
    short_url = f"{request.host_url}t/{short_code}"
    # Return complete order details
    return jsonify({
        "order_id": order.order_id,
        "status": order.status,
        "order_date": order.timestamp.strftime("%B %d, %Y at %H:%M"),
        "customer": {
            "id": order.customer.customer_id,
            "name": order.customer.name,
            "email": order.customer.email
        },
        "flower": {
            "name": order.flower.name,
            "price": order.flower.price,
            "image_url": order.flower.image_url,
            "available_stock": order.flower.available_stock,
            "committed_stock": order.flower.committed_stock
        },
        "quantity": order.quantity,
        "total_price": order.total_price,
        "tracking": {
            "full_url": tracking_url,
            "share_link": short_url,
            "short_code": short_code
        }
    }), 200


@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """
     API endpoint to shorten a URL.
     System generates short, shareable link
    """
    try:
        data = request.json
        # Validate input
        if not data or 'url' not in data:
            return jsonify({

                'success': False,
                'error': 'Missing required field: url'
            }), 400

        original_url = data['url']
        purpose = data.get('purpose', 'general')

        # Generate short code
        short_code = url_shortener.shorten(original_url, purpose)

        # Build full short URL
        # Use request.host_url to get the base URL (http://localhost:5000/)
        short_url = f"{request.host_url}t/{short_code}"

        return jsonify({

            'success': True,
            'original_url': original_url,
            'short_code': short_code,
            'short_url': short_url,
            'purpose': purpose
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/t/<short_code>')
def redirect_short_url(short_code):
    """
    Redirect endpoint for shortened URLs.
    This endpoint looks up the original URL
    Browser redirects to original URL

    Example:
    GET /t/aB3xK9  →  Redirects to: /orders/details?order_id=10492
    """
    # Look up the original URL
    original_url = url_shortener.expand(short_code)

    if original_url:
        # Redirect to the original URL
        # Status code 302 = temporary redirect (standard for URL shorteners)
        return redirect(original_url, code=302)
    else:
        # Short code not found
        return jsonify({
            'error': 'Link not found',
            'message': 'This shortened link does not exist or has expired.'
        }), 404


@app.route('/api/link-stats/<short_code>')
def get_link_stats(short_code):
    """
    Get analytics for a shortened URL.
    """
    stats = url_shortener.get_stats(short_code)
    if stats:
        return jsonify({
            'short_code': short_code,
            'original_url': stats['url'],
            'purpose': stats['purpose'],
            'click_count': stats['click_count'],
            'created_at': stats['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        }), 200
    else:
        return jsonify({
            'error': 'Link not found'
        }), 404


"""@app.route('/test-shortener')
def test_shortener():
    test_url = "http://localhost:5000/flowers"
    short_code = url_shortener.shorten(test_url, "test")
    expanded = url_shortener.expand(short_code)

    return jsonify({
        'original': test_url,
        'short_code': short_code,
        'expanded': expanded,
        'match': expanded == test_url
    })
"""

# Runs the Flask server only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
