from typing import List
from repositories.base import BaseRepository
from models.product import Product

class ProductRepository(BaseRepository):
    def get_all(self) -> List[Product]:
        query = "SELECT * FROM products ORDER BY name ASC"
        rows = self.execute_query(query)
        products = []
        
        for row in rows:
            products.append(
                Product(
                    product_id=row['product_id'],
                    category_id=row['category_id'],
                    name=row['name'],
                    brand=row['brand'],
                    price=row['price'],
                    cost_price=row['cost_price'],
                    stock_quantity=row['stock_quantity'],
                    min_stock_level=row['min_stock_level'],
                    size=row.get('size'),
                    description=row.get('description')
                )
            )
        return products

    def get_by_category(self, category_id: int) -> List[Product]:
        query = "SELECT * FROM products WHERE category_id = %s ORDER BY name ASC"
        rows = self.execute_query(query, (category_id,))
        products = []

        for row in rows:
            products.append(
                Product(
                    product_id=row['product_id'],
                    category_id=row['category_id'],
                    name=row['name'],
                    brand=row['brand'],
                    price=float(row['price']),
                    cost_price=float(row['cost_price']),
                    stock_quantity=row['stock_quantity'],
                    min_stock_level=row.get('min_stock_level'),
                    size=row.get('size'),
                    description=row.get('description')
                )
            )
        return products

    def search(self, search_term: str) -> List[Product]:
        query = "SELECT * FROM products WHERE name LIKE %s OR brand LIKE %s ORDER BY name ASC"
        term = f"%{search_term}%"
        rows = self.execute_query(query, (term, term))
        products = []

        for row in rows:
            products.append(
                Product(
                    product_id=row['product_id'],
                    category_id=row['category_id'],
                    name=row['name'],
                    brand=row['brand'],
                    price=float(row['price']),
                    cost_price=float(row['cost_price']),
                    stock_quantity=row['stock_quantity'],
                    min_stock_level=row.get('min_stock_level'),
                    size=row.get('size'),
                    description=row.get('description')
                )
            )
        return products

    def update_stock(self, product_id: int, quantity_delta: int) -> bool:
        query = """UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s"""
        return self.execute_statement(query, (quantity_delta, product_id))