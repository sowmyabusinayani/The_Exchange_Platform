from models.flower import Flower
from models.customer import Customer
from datetime import datetime


class Order:
    def __init__(self, order_id, customer, flower, quantity):
        self.order_id = order_id
        self.customer = customer
        self.flower = flower
        self.quantity = quantity
        self.total_price = self.flower.price * quantity
        self.status = "Pending"
        self.timestamp = datetime.now()

    def place_order(self):
        """
        Attempts to finalize the order.
        1. Asks the Flower model to move stock from 'Available' to 'Committed'.
        2. Updates the order status based on the result.
        """
        stock_reserved = self.flower.update_stock(self.quantity)
        if stock_reserved:
            self.status = "Confirmed"
            return True, "Order confirmed. Stock committed for shipment."
        else:
            self.status = "Failed"
            return False, f"Insufficient stock for {self.flower.name}"

    def to_dict(self):
        # Returns order details for the Admin Dashboard or History.
        return {
            "order_id": self.order_id,
            "customer": {
                "customer_id": self.customer.customer_id,
                "name": self.customer.name
            },
            "flower": {
                "name": self.flower.name,
                "price": self.flower.price,
                "available_stock": self.flower.available_stock
            },
            "quantity": self.quantity,
            "status": self.status,
            "date": self.timestamp.strftime("%Y-%m-%d %H:%M")
        }

    def __repr__(self) -> str:
        return (
            f"Order(id={self.order_id}, customer={self.customer.name}, "
            f"flower={self.flower.name}, quantity={self.quantity}, status={self.status})"
        )
