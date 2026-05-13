import csv
import os
import pydgraph
import json
import uuid
from datetime import datetime
from connect import get_mongo_db, get_dgraph_client, get_cassandra_session

# Cassandra
def populate_cassandra():
    session = get_cassandra_session(keyspace=None)
    
    cql_path = os.path.join(os.path.dirname(__file__), "Cassandra", "schema.cql")
    with open(cql_path, 'r', encoding="utf-8") as f:
        full_sql = f.read()
        commands = full_sql.split(';')
        for cmd in commands:
            clean_cmd = cmd.strip()
            if clean_cmd:
                session.execute(clean_cmd)
    
    session.set_keyspace('mercado_cerrado_logs')
    DATA_DIR_C = os.path.join(os.path.dirname(__file__), "data", "Cassandra")

    # --- Product Views (RF1) ---
    with open(os.path.join(DATA_DIR_C, "product_views.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = "INSERT INTO product_views_by_user (user_id, view_timestamp, product_id, category, price) VALUES (%s, %s, %s, %s, %s)"
            session.execute(query, [uuid.UUID(row['user_id']), datetime.strptime(row['view_timestamp'], "%Y-%m-%d %H:%M:%S"), uuid.UUID(row['product_id']), row['category'], float(row['price'])])
    
    # --- Searches (RF2) ---
    with open(os.path.join(DATA_DIR_C, "searches.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = "INSERT INTO search_history_by_user (user_id, search_timestamp, query, results_count) VALUES (%s, %s, %s, %s)"
            session.execute(query, [uuid.UUID(row['user_id']), datetime.strptime(row['search_timestamp'], "%Y-%m-%d %H:%M:%S"), row['query'], int(row['results_count'])])

    # --- Purchases (RF3) ---
    with open(os.path.join(DATA_DIR_C, "purchases.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products = row['product_names'].split(";")
            query = "INSERT INTO purchase_history_by_user (user_id, purchase_timestamp, order_id, product_names, total_amount) VALUES (%s, %s, %s, %s, %s)"
            session.execute(query, [uuid.UUID(row['user_id']), datetime.strptime(row['purchase_timestamp'], "%Y-%m-%d %H:%M:%S"), uuid.UUID(row['order_id']), products, float(row['total_amount'])])

    # --- Logins (RF4) ---
    with open(os.path.join(DATA_DIR_C, "logins.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = "INSERT INTO login_logs_by_user (user_id, login_timestamp, ip_address, device) VALUES (%s, %s, %s, %s)"
            session.execute(query, [uuid.UUID(row['user_id']), datetime.strptime(row['login_timestamp'], "%Y-%m-%d %H:%M:%S"), row['ip_address'], row['device']])

    # --- Cart Activity (RF5) ---
    with open(os.path.join(DATA_DIR_C, "cart_activity.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = "INSERT INTO cart_activity_by_user (user_id, activity_timestamp, action, product_id, quantity) VALUES (%s, %s, %s, %s, %s)"
            session.execute(query, [uuid.UUID(row['user_id']), datetime.strptime(row['activity_timestamp'], "%Y-%m-%d %H:%M:%S"), row['action'], uuid.UUID(row['product_id']), int(row['quantity'])])

    # --- Price Changes (RF6) ---
    with open(os.path.join(DATA_DIR_C, "price_changes.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = "INSERT INTO price_changes_by_product (product_id, change_timestamp, old_price, new_price, discount_pct) VALUES (%s, %s, %s, %s, %s)"
            session.execute(query, [uuid.UUID(row['product_id']), datetime.strptime(row['change_timestamp'], "%Y-%m-%d %H:%M:%S"), float(row['old_price']), float(row['new_price']), float(row['discount_pct'])])

    # --- Favorites (RF7) ---
    with open(os.path.join(DATA_DIR_C, "favorites.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = "INSERT INTO favorite_activity_by_user (user_id, fav_timestamp, product_id, note) VALUES (%s, %s, %s, %s)"
            session.execute(query, [uuid.UUID(row['user_id']), datetime.strptime(row['fav_timestamp'], "%Y-%m-%d %H:%M:%S"), uuid.UUID(row['product_id']), row['note']])

    print("\n✓ Populate completado en Cassandra.")

def drop_all_cassandra():
    session = get_cassandra_session()
    tables = [
        "product_views_by_user", "search_history_by_user", "purchase_history_by_user",
        "login_logs_by_user", "cart_activity_by_user", "price_changes_by_product",
        "favorite_activity_by_user"
    ]
    for t in tables:
        session.execute(f"TRUNCATE {t}")
    print("✓ Todas las tablas de Cassandra han sido vaciadas.")

# MongoDB

db = get_mongo_db()
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "Mongo")
DATA_DIR_D = os.path.join(os.path.dirname(__file__), "data", "Dgraph")


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

# Dgraph
def populate_dgraph():
    client = get_dgraph_client()
    
    txn = client.txn()
    try:
        for tipo in ["Product", "User", "Category", "Review", "Order"]:
            res = txn.query(f"{{ nodos(func: type({tipo})) {{ uid }} }}")
            uids = [{"uid": n["uid"]} for n in json.loads(res.json).get("nodos", [])]
            if uids:
                txn.mutate(del_obj=uids)
        txn.commit()
    except Exception as e:
        print(f"Error al limpiar Dgraph: {e}")
    finally:
        txn.discard()

    # Schema
    schema = """
    type User {
        name: string
        email: string
        is_frequent: bool
        bought: [uid]
        wrote_review: [uid]
        placed: [uid]
        purchased: [uid]
        rated: [uid]
    }
    
    type Product {
        name: string
        price: float
        is_new: bool
        belongs_to: [uid]
    }
    
    type Category {
        category_name: string
    }
    
    type Review {
        rating: int
        text: string
        date: datetime
        review_for: [uid]
    }
    
    type Order {
        order_date: datetime
        total: float
        contains: [uid]
    }

    name: string @index(exact, term) .
    email: string @index(hash) .
    is_frequent: bool @index(bool) .
    price: float @index(float) .
    is_new: bool @index(bool) .
    rating: int @index(int) .
    date: datetime @index(hour) .
    order_date: datetime @index(hour) .
    category_name: string @index(exact, term) .
    text: string .
    total: float .

    bought: [uid] @reverse .
    contains: [uid] @reverse .
    belongs_to: [uid] @reverse .
    placed: [uid] @reverse .
    wrote_review: [uid] .
    review_for: [uid] .
    purchased: [uid] .
    rated: [uid] .
    """
    client.alter(pydgraph.Operation(schema=schema))
    
    counts = {"categories": 0, "users": 0, "products": 0, "reviews": 0, "orders": 0}
    mutations = []

    # --- Categories ---
    with open(os.path.join(DATA_DIR_D, "categories.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mutations.append({"uid": f"_:{row['id_cat']}", "dgraph.type": "Category", "category_name": row['name']})
            counts["categories"] += 1

    # --- Users ---
    with open(os.path.join(DATA_DIR_D, "user.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mutations.append({
                "uid": f"_:{row['id_user']}", "dgraph.type": "User",
                "name": row['name'], "email": row['email'], "is_frequent": row['is_frequent'].lower() == 'true'
            })
            counts["users"] += 1

    # --- Products ---
    with open(os.path.join(DATA_DIR_D, "product.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mutations.append({
                "uid": f"_:{row['id_prod']}", "dgraph.type": "Product",
                "name": row['name'], "price": float(row['price']), "is_new": row['is_new'].lower() == 'true',
                "belongs_to": {"uid": f"_:{row['id_cat']}"} 
            })
            counts["products"] += 1

    # --- Reviews ---
    with open(os.path.join(DATA_DIR_D, "reviews.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mutations.append({
                "uid": f"_:{row['id_user']}",
                "wrote_review": {
                    "uid": f"_:{row['id_review']}", "dgraph.type": "Review",
                    "rating": int(row['rating']), "text": row['text'], "date": row['date'],
                    "review_for": {"uid": f"_:{row['id_prod']}"}
                },
                "rated": {"uid": f"_:{row['id_prod']}"}
            })
            counts["reviews"] += 1

    # --- Orders ---
    with open(os.path.join(DATA_DIR_D, "order.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mutations.append({
                "uid": f"_:{row['id_user']}",
                "bought": {"uid": f"_:{row['id_prod']}"},
                "purchased": {"uid": f"_:{row['id_prod']}"},
                "placed": {
                    "uid": f"_:{row['id_order']}", "dgraph.type": "Order",
                    "order_date": row['order_date'], "total": float(row['total']),
                    "contains": {"uid": f"_:{row['id_prod']}"}
                }
            })
            counts["orders"] += 1

    txn = client.txn()
    try:
        txn.mutate(set_obj=mutations)
        txn.commit()
        print(f"  categories: {counts['categories']} nodos insertados.")
        print(f"  users: {counts['users']} nodos insertados.")
        print(f"  products: {counts['products']} nodos insertados.")
        print(f"  reviews: {counts['reviews']} nodos insertados.")
        print(f"  orders: {counts['orders']} nodos insertados.")
        print("\n✓ Populate completado en Dgraph.")
        
    except Exception as e:
        print(f"\nError al insertar en Dgraph: {e}")
    finally:
        txn.discard()

def drop_all_dgraph():
    client = get_dgraph_client()
    op = pydgraph.Operation(drop_all=True)
    client.alter(op)
    print("✓ Toda la base de datos Dgraph eliminada.")

if __name__ == "__main__":
    populate_mongo()
    populate_dgraph()
