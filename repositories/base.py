from database import get_connection

class BaseRepository:
    def execute_query(self, query: str, params: tuple = ()):
        conn = get_connection()

        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result if result is not None else []
        finally:
            cursor.close()
            conn.close()

    def execute_statement(self, query: str, params: tuple = ()) -> bool:
        conn = get_connection()

        if not conn:
            return False
        
        cursor = conn.cursor()

        try:
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Database error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()