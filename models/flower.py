class Flower:
    def __init__(self, name, price, initial_Stock):
        self.name = name
        self.price = price
        self.initial_Stock = initial_Stock
        self.committed_stock = 0

    def update_stock(self, quantity):
        self.initial_Stock = self.initial_Stock - quantity

    def to_dict(self):
        return {"name": self.name, "price": self.price, "initial_Stock ": self.initial_Stock}

    def __repr__(self) -> str:
        return f"Flower(name={self.name}, price={self.price}, initial_Stock ={self.initial_Stock })"
