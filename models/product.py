from dataclasses import dataclass

@dataclass
class Product:
    product_id: int | None
    category_id: int
    name: str
    brand: str
    price: float
    cost_price: float
    stock_quantity: int
    min_stock_level: int | None = None
    size: str | None = None
    description: str | None = None

    @property
    def low_stock(self) -> bool:
        return 0 < self.stock_quantity <= self.min_stock_level

    @property
    def out_of_stock(self) -> bool:
        return self.stock_quantity <= 0