from typing import List, Optional
from models.category import Category
from repositories.base import BaseRepository

class CategoryRepository(BaseRepository):
    def get_all(self) -> List[Category]:
        query = "SELECT category_id, name FROM categories ORDER BY name ASC"
        rows = self.execute_query(query)
        categories = []

        for row in rows:
            categories.append(
                Category(
                    category_id=row['category_id'],
                    name=row['name']
                )
            )
        return categories

    def get_by_id(self, category_id: int) -> Optional[Category]:
        query = "SELECT category_id, name FROM categories WHERE category_id = %s"
        rows = self.execute_query(query, (category_id,))
        if rows:
            row = rows[0]
            return Category(
                category_id=row['category_id'],
                name=row['name']
            )
        return None

    def create(self, name: str) -> int:
        query = "INSERT INTO categories (name) VALUES (%s)"
        return self.execute_statement(query, (name,))

    def update(self, category_id: int, name: str) -> bool:
        query = "UPDATE categories SET name = %s WHERE category_id = %s"
        return self.execute_statement(query, (name, category_id))

    def delete(self, category_id: int) -> bool:
        query = "DELETE FROM categories WHERE category_id = %s"
        return self.execute_statement(query, (category_id,))
