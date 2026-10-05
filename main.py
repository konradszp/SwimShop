from repositories import ProductRepository

def main():
    print("SwimShop POS system is starting...")

    product_rep = ProductRepository()
    products = product_rep.get_all()

    print(f"\n--- Product Inventory ({len(products)} items found) ---")
    for p in products:
        status = "OUT OF STOCK" if p.out_of_stock else ("LOW STOCK" if p.low_stock else "OK")
        print(f"[{status}] {p.name} ({p.brand}) - ${p.price:.2f} | Stock: {p.stock_quantity}")

if __name__ == "__main__":
    main()