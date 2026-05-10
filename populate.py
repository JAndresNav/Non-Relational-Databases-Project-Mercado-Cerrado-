import csv
import os
from datetime import datetime
from connect import get_mongo_db

# MongoDB

db = get_mongo_db()
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "Mongo")


def populate_mongo():
    # Drop existing collections
    for col in ["products", "users", "carts", "wishlists", "user_preferences"]:
        db[col].drop()

    # --- Products ---
    with open(os.path.join(DATA_DIR, "products.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        products = []
        for row in reader:
            products.append({
                "name": row["name"],
                "description": row["description"],
                "category": row["category"],
                "price": float(row["price"]),
                "stock": int(row["stock"]),
                "image": row["image"],
                "attributes": {
                    "material": row["attr_material"],
                    "dimensions": row["attr_dimensions"],
                    "warranty": row["attr_warranty"],
                },
            })
        db.products.insert_many(products)
        print(f"  products: {len(products)} documentos insertados.")

    # --- Users ---
    with open(os.path.join(DATA_DIR, "users.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        users = []
        for row in reader:
            users.append({
                "name": row["name"],
                "email": row["email"],
                "created_at": datetime.strptime(row["created_at"], "%Y-%m-%d"),
                "account_status": row["account_status"],
                "address": {
                    "street": row["addr_street"],
                    "city": row["addr_city"],
                    "zip": row["addr_zip"],
                },
            })
        db.users.insert_many(users)
        print(f"  users: {len(users)} documentos insertados.")

    # Build lookup maps
    user_map = {u["email"]: u["_id"] for u in db.users.find({}, {"email": 1})}
    product_map = {p["name"]: p["_id"] for p in db.products.find({}, {"name": 1})}

    # --- Carts ---
    with open(os.path.join(DATA_DIR, "carts.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        carts = []
        for row in reader:
            items = []
            total = 0.0
            for item_str in row["items"].split(";"):
                name, price, qty = item_str.rsplit(":", 2)
                price, qty = float(price), int(qty)
                subtotal = price * qty
                items.append({
                    "product_id": product_map.get(name),
                    "name": name,
                    "price": price,
                    "quantity": qty,
                    "subtotal": subtotal,
                })
                total += subtotal
            carts.append({
                "user_id": user_map.get(row["user_email"]),
                "items": items,
                "total": total,
                "cart_status": row["cart_status"],
                "updated_at": datetime.now(),
            })
        db.carts.insert_many(carts)
        print(f"  carts: {len(carts)} documentos insertados.")

    # --- Wishlists ---
    with open(os.path.join(DATA_DIR, "wishlists.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        wishlists = []
        for row in reader:
            product_ids = [product_map.get(n) for n in row["product_names"].split(";")]
            wishlists.append({
                "user_id": user_map.get(row["user_email"]),
                "products": product_ids,
            })
        db.wishlists.insert_many(wishlists)
        print(f"  wishlists: {len(wishlists)} documentos insertados.")

    # --- User Preferences ---
    with open(os.path.join(DATA_DIR, "user_preferences.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        prefs = []
        for row in reader:
            prefs.append({
                "user_id": user_map.get(row["user_email"]),
                "favorite_categories": row["favorite_categories"].split(";"),
                "price_range": {
                    "min": float(row["price_min"]),
                    "max": float(row["price_max"]),
                },
                "last_update": datetime.now(),
            })
        db.user_preferences.insert_many(prefs)
        print(f"  user_preferences: {len(prefs)} documentos insertados.")

    print("\n✓ Populate completado.")


def drop_all_mongo():
    for col in ["products", "users", "carts", "wishlists", "user_preferences"]:
        db[col].drop()
    print("✓ Todas las colecciones de MongoDB eliminadas.")


if __name__ == "__main__":
    populate_mongo()
