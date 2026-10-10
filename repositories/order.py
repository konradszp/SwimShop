from database import get_connection
from models.order import Order, OrderItem, OrderStatus

class OrderRepository:

    def create_order(self, order: Order) -> int | None:
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO orders (customer_id, user_id, order_datetime, total_amount, status) VALUES (%s, %s, %s, %s, %s)",
                (order.customer_id,order.user_id,order.order_datetime,order.total_amount,order.status.value),
            )
            order_id = cursor.lastrowid

            for item in order.items:
                cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s,%s,%s,%s)",
                    (order_id, item.product_id, item.quantity, item.unit_price),               
                )
                cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                    (item.quantity, item.product_id),               
                )

            conn.commit()
            return order_id

        except Exception as e:
            conn.rollback()
            print(f"[OrderRepository Error] Failed to create an order: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, order_id: int) -> Order | None:
        conn = get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            order_data = cursor.fetchone()
            if not order_data:
                return None

            cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
            order_items_data = cursor.fetchall()

            items = []

            for item in order_items_data:
                items.append(
                    OrderItem(
                        order_item_id=item["order_item_id"],
                        order_id=item["order_id"],
                        product_id=item["product_id"],
                        quantity=item["quantity"],
                        unit_price=float(item["unit_price"]),
                    )
                )

            return Order(
                order_id=order_data["order_id"],
                customer_id=order_data["customer_id"],
                user_id=order_data["user_id"],
                order_datetime=order_data["order_datetime"],
                total_amount=float(order_data["total_amount"]),
                status=OrderStatus(order_data["status"]),
                items=items,
            )

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def get_all(self) -> list[Order]:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM orders ORDER BY order_datetime DESC")
            orders_data = cursor.fetchall()

            orders = []
            for order in orders_data:
                orders.append(
                    Order(
                        order_id=order["order_id"],
                        customer_id=order["customer_id"],
                        user_id=order["user_id"],
                        order_datetime=order["order_datetime"],
                        total_amount=float(order["total_amount"]),
                        status=OrderStatus(order["status"]),
                        items=[]
                    )
                )
            return orders
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


