from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    PENDING = 'pending'

@dataclass
class OrderItem:
    product_id: int
    quantity: int
    unit_price: float
    order_item_id: int | None = None
    order_id: int | None = None

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

@dataclass
class Order:
    customer_id: int
    user_id: int
    order_datetime: datetime
    total_amount: float
    status: OrderStatus
    order_id: int | None = None
    items: list[OrderItem]= field(default_factory=list)
    