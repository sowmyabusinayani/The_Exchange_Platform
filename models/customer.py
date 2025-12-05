class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name

    def to_dict(self) -> dict:
        return {"customer_id": self.customer_id, "name": self.name}

    def __repr__(self) -> str:
        return f"Customer(id={self.customer_id}, name={self.name})"
