from repositories.base import BaseRepository
from models.user import User, UserRole
from utils.security import hash_password, verify_password


class UserRepository(BaseRepository):
    def get_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s;"
        rows = self.execute_query(query, (username,))
        if rows:
            row = rows[0]
            return User(
                user_id=row['user_id'],
                username=row['username'],
                password_hash=row['password_hash'],
                full_name=row['full_name'],
                role=UserRole(row['role'])
            )
        return None

    def authenticate(self, username, password):
        user = self.get_by_username(username)
        if user and verify_password(password, user.password_hash):
            return user
        return None

    def create_user(self, username: str, password: str, full_name: str, role: UserRole) -> bool:
        hashed_password = hash_password(password)
        query = """
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES (%s, %s, %s, %s);"""
        return self.execute_statement(query, (username, hashed_password, full_name, role.value))

    def delete_user(self, user_id: int) -> bool:
        query = "DELETE FROM users WHERE user_id = %s;"
        return self.execute_statement(query, (user_id,))