from models.flower import Flower
from models.customer import Customer


class Order:
    def __init__(self, order_id, customer, flower, quantity):
        self.order_id = order_id
        self.customer = customer
        self.flower = flower
        self.quantity = quantity
        self.status = "Pending"

    def place_order(self):
        if self.flower.initial_Stock >= self.quantity:
            self.flower.update_stock(self.quantity)
            self.status = "Confirmed"
            print("The order placed by the customer has been ", self.status)
        else:
            self.status = "Out of Stock"

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer": {
                "customer_id": self.customer.customer_id,
                "name": self.customer.name
            },
            "flower": {
                "name": self.flower.name,
                "price": self.flower.price,
                "stock": self.flower.initial_Stock
            },
            "quantity": self.quantity,
            "status": self.status
        }

    def __repr__(self) -> str:
        return (
            f"Order(id={self.order_id}, customer={self.customer.name}, "
            f"flower={self.flower.name}, quantity={self.quantity}, status={self.status})"
        )
