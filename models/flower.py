class Flower:
    def __init__(self, flower_id, name, price, initial_stock, image_url):
        self.flower_id = flower_id
        self.name = name
        self.price = price
        # Physical stock ready to be sold.
        self.available_stock = initial_stock
        # Stock sold but waiting for shipment
        self.committed_stock = 0
        self.image_url = image_url

    def update_stock(self, quantity):
        """
        Updates stock based on an order.
        Moves stock from 'Available' to 'Committed'.
        """
        if self.available_stock >= quantity:
            self.available_stock -= quantity  # Reduce available stock
            self.committed_stock += quantity  # Increasing committed stock
            return True
        return False

    def to_dict(self):
        # Converts object to dictionary for API JSON response.
        return {
            "id": self.flower_id,
            "name": self.name,
            "price": self.price,
            "stock": self.available_stock,
            "committed_stock": self.committed_stock,
            "img": self.image_url
        }

    def __repr__(self) -> str:
        return f"Flower(name={self.name}, price={self.price}, available_stock ={self.available_stock})"
