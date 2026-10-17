from models.product import Product

class CartItem:
    def __init__(self, product: Product):
        self.product = product
        self.quantity = 1

    @property
    def total_price(self) -> float:
        return self.product.price * self.quantity

class Cart:
    def __init__(self):
        self.items: dict[int, CartItem] = {}

    def add_product(self, product: Product) -> tuple[bool, str]:
        product_id = product.product_id
        if product_id in self.items:
            if self.items[product_id].quantity < product.stock_quantity:
                self.items[product_id].quantity += 1
                return True, "Increased quantity"
            return False, "Maximum available stock reached"
        else:
            if product.stock_quantity > 0:
                self.items[product_id] = CartItem(product)
                return True, "Added to cart"
            return False, "Item is out of stock"

    def update_quantity(self, product_id: int, delta: int, stock_limit: int) -> bool:
        if product_id in self.items:
            new_quantity = self.items[product_id].quantity + delta
            if new_quantity > stock_limit:
                return False
            self.items[product_id].quantity = new_quantity
            if self.items[product_id].quantity <= 0:
                del self.items[product_id]
        return True

    def clear(self):
        self.items.clear()

    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items.values())

    