from dataclasses import dataclass

@dataclass
class Customer:
    customer_id: int
    full_name: str
    email: str
    phone: int
    address: str