from database import get_connection
from models.customer import Customer

class CustomerRepository:

    def get_all(self) -> list[Customer]:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM customers")
            customers_data = cursor.fetchall()

            customers = []

            for customer in customers_data:
                customers.append(
                    Customer(
                        customer_id=customer["customer_id"],
                        full_name=customer["full_name"],
                        email=customer["email"],
                        phone=customer["phone"],
                        address=customer["address"]
                    )
                )
            return customers

        finally:
            try:
                if cursor:
                    cursor.close()
            except Exception:
                pass
                
            try:
                if conn:
                    conn.close()
            except Exception:
                pass

        
        