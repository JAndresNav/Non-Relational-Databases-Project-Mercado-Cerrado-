from datetime import datetime
from connect import get_mongo_db

db = get_mongo_db()

RF_DESCRIPTIONS = {
    1: "RF1 - Catálogo de Productos: Almacenar la información general de cada producto disponible en la tienda.\n  Colección: products | Campos: name, category, price, stock, image, description, attributes",
    2: "RF2 - Perfil General del Usuario: Guardar la información básica de cada usuario dentro de la plataforma.\n  Colección: users | Campos: name, email, created_at, account_status, address",
    3: "RF3 - Carrito de Compras Activo: Almacenar el estado actual del carrito de cada usuario, incluyendo productos, cantidades y total.\n  Colección: carts | Campos: user_id, items[], total, updated_at, cart_status",
    4: "RF4 - Lista de Deseos: Permitir que el usuario guarde productos de interés para comprarlos posteriormente.\n  Colección: wishlists | Campos: user_id, products[]",
    5: "RF5 - Preferencias Generales del Usuario: Guardar información básica de gustos del usuario para personalizar la experiencia.\n  Colección: user_preferences | Campos: user_id, favorite_categories, price_range, last_update",
    6: "RF6 - Índices para Optimización: Implementar índices en las colecciones principales para mejorar la velocidad de búsqueda.\n  Índices: users.email (unique), products.category+price (compound), products.name (text), carts.user_id, user_preferences.user_id",
    7: "RF7 - Pipeline de Agregación: Utilizar un pipeline de agregación para analizar los productos más almacenados en carritos.\n  Pipeline: $match → $unwind → $group → $sort → $limit 10",
}


# ==================== RF1: Catálogo de Productos ====================

def rf1_menu():
    while True:
        print("\n--- RF1: Catálogo de Productos ---")
        print("1. Ver todos los productos")
        print("2. Buscar por categoría")
        print("3. Buscar por nombre")
        print("4. Buscar por rango de precio")
        print("9. Ver requerimiento funcional")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        if opt == "1":
            for p in db.products.find():
                print(f"  {p['name']} | {p['category']} | ${p['price']} | Stock: {p['stock']}")
        elif opt == "2":
            cat = input("Categoría: ")
            for p in db.products.find({"category": cat}):
                print(f"  {p['name']} | ${p['price']} | Stock: {p['stock']}")
        elif opt == "3":
            name = input("Nombre (búsqueda parcial): ")
            for p in db.products.find({"name": {"$regex": name, "$options": "i"}}):
                print(f"  {p['name']} | {p['category']} | ${p['price']}")
        elif opt == "4":
            min_p = float(input("Precio mínimo: "))
            max_p = float(input("Precio máximo: "))
            for p in db.products.find({"price": {"$gte": min_p, "$lte": max_p}}):
                print(f"  {p['name']} | ${p['price']} | {p['category']}")
        elif opt == "9":
            print(f"\n  {RF_DESCRIPTIONS[1]}")
        elif opt == "0":
            break


# ==================== RF2: Perfil General del Usuario ====================

def rf2_menu():
    while True:
        print("\n--- RF2: Perfil General del Usuario ---")
        print("1. Ver todos los usuarios")
        print("2. Buscar por email")
        print("3. Buscar por nombre")
        print("4. Filtrar por estado de cuenta")
        print("9. Ver requerimiento funcional")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        if opt == "1":
            for u in db.users.find():
                print(f"  {u['name']} | {u['email']} | {u['account_status']} | {u['address']['city']}")
        elif opt == "2":
            email = input("Email: ")
            u = db.users.find_one({"email": email})
            if u:
                print(f"  Nombre: {u['name']}")
                print(f"  Email: {u['email']}")
                print(f"  Estado: {u['account_status']}")
                print(f"  Dirección: {u['address']['street']}, {u['address']['city']} {u['address']['zip']}")
                print(f"  Creado: {u['created_at']}")
            else:
                print("  Usuario no encontrado.")
        elif opt == "3":
            name = input("Nombre (búsqueda parcial): ")
            for u in db.users.find({"name": {"$regex": name, "$options": "i"}}):
                print(f"  {u['name']} | {u['email']} | {u['account_status']}")
        elif opt == "4":
            status = input("Estado (active/suspended): ")
            for u in db.users.find({"account_status": status}):
                print(f"  {u['name']} | {u['email']}")
        elif opt == "9":
            print(f"\n  {RF_DESCRIPTIONS[2]}")
        elif opt == "0":
            break


# ==================== RF3: Carrito de Compras Activo ====================

def rf3_menu():
    while True:
        print("\n--- RF3: Carrito de Compras Activo ---")
        print("1. Ver carrito activo de un usuario")
        print("2. Agregar producto al carrito")
        print("3. Eliminar producto del carrito")
        print("4. Convertir carrito (checkout)")
        print("9. Ver requerimiento funcional")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        if opt == "1":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            cart = db.carts.find_one({"user_id": user["_id"], "cart_status": "active"})
            if not cart:
                print("  No tiene carrito activo.")
            else:
                for item in cart["items"]:
                    print(f"  {item['name']} | ${item['price']} x{item['quantity']} = ${item['subtotal']}")
                print(f"  Total: ${cart['total']}")
        elif opt == "2":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            cart = db.carts.find_one({"user_id": user["_id"], "cart_status": "active"})
            if not cart:
                cart_id = db.carts.insert_one({"user_id": user["_id"], "items": [], "total": 0.0, "cart_status": "active", "updated_at": datetime.now()}).inserted_id
            else:
                cart_id = cart["_id"]
            prod_name = input("Nombre del producto: ")
            product = db.products.find_one({"name": {"$regex": prod_name, "$options": "i"}})
            if not product:
                print("  Producto no encontrado.")
                continue
            qty = int(input("Cantidad: "))
            subtotal = product["price"] * qty
            db.carts.update_one({"_id": cart_id}, {
                "$push": {"items": {"product_id": product["_id"], "name": product["name"], "price": product["price"], "quantity": qty, "subtotal": subtotal}},
                "$inc": {"total": subtotal},
                "$set": {"updated_at": datetime.now()}
            })
            print(f"  ✓ {product['name']} x{qty} agregado al carrito.")
        elif opt == "3":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            cart = db.carts.find_one({"user_id": user["_id"], "cart_status": "active"})
            if not cart:
                print("  No tiene carrito activo.")
                continue
            prod_name = input("Nombre del producto a eliminar: ")
            item = next((i for i in cart["items"] if i["name"].lower() == prod_name.lower()), None)
            if not item:
                print("  Producto no está en el carrito.")
                continue
            db.carts.update_one({"_id": cart["_id"]}, {
                "$pull": {"items": {"name": item["name"]}},
                "$inc": {"total": -item["subtotal"]},
                "$set": {"updated_at": datetime.now()}
            })
            print(f"  ✓ {item['name']} eliminado del carrito.")
        elif opt == "4":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            result = db.carts.update_one({"user_id": user["_id"], "cart_status": "active"}, {"$set": {"cart_status": "converted", "updated_at": datetime.now()}})
            if result.modified_count:
                print("  ✓ Carrito convertido (checkout completado).")
            else:
                print("  No tiene carrito activo.")
        elif opt == "9":
            print(f"\n  {RF_DESCRIPTIONS[3]}")
        elif opt == "0":
            break


# ==================== RF4: Lista de Deseos (Wishlist) ====================

def rf4_menu():
    while True:
        print("\n--- RF4: Lista de Deseos ---")
        print("1. Ver wishlist de un usuario")
        print("2. Agregar producto a wishlist")
        print("3. Eliminar producto de wishlist")
        print("9. Ver requerimiento funcional")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        if opt == "1":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            wl = db.wishlists.find_one({"user_id": user["_id"]})
            if not wl or not wl["products"]:
                print("  Wishlist vacía.")
            else:
                for pid in wl["products"]:
                    p = db.products.find_one({"_id": pid})
                    if p:
                        print(f"  {p['name']} | ${p['price']} | {p['category']}")
        elif opt == "2":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            prod_name = input("Nombre del producto: ")
            product = db.products.find_one({"name": {"$regex": prod_name, "$options": "i"}})
            if not product:
                print("  Producto no encontrado.")
                continue
            wl = db.wishlists.find_one({"user_id": user["_id"]})
            if not wl:
                db.wishlists.insert_one({"user_id": user["_id"], "products": [product["_id"]]})
            else:
                db.wishlists.update_one({"_id": wl["_id"]}, {"$addToSet": {"products": product["_id"]}})
            print(f"  ✓ {product['name']} agregado a wishlist.")
        elif opt == "3":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            prod_name = input("Nombre del producto a eliminar: ")
            product = db.products.find_one({"name": {"$regex": prod_name, "$options": "i"}})
            if not product:
                print("  Producto no encontrado.")
                continue
            result = db.wishlists.update_one({"user_id": user["_id"]}, {"$pull": {"products": product["_id"]}})
            if result.modified_count:
                print(f"  ✓ {product['name']} eliminado de wishlist.")
            else:
                print("  Producto no estaba en la wishlist.")
        elif opt == "9":
            print(f"\n  {RF_DESCRIPTIONS[4]}")
        elif opt == "0":
            break


# ==================== RF5: Preferencias Generales del Usuario ====================

def rf5_menu():
    while True:
        print("\n--- RF5: Preferencias del Usuario ---")
        print("1. Ver preferencias de un usuario")
        print("2. Actualizar categorías favoritas")
        print("3. Actualizar rango de precio")
        print("9. Ver requerimiento funcional")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        if opt == "1":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            pref = db.user_preferences.find_one({"user_id": user["_id"]})
            if not pref:
                print("  Sin preferencias registradas.")
            else:
                print(f"  Categorías favoritas: {', '.join(pref['favorite_categories'])}")
                print(f"  Rango de precio: ${pref['price_range']['min']} - ${pref['price_range']['max']}")
                print(f"  Última actualización: {pref['last_update']}")
        elif opt == "2":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            cats = input("Categorías (separadas por ;): ").split(";")
            db.user_preferences.update_one(
                {"user_id": user["_id"]},
                {"$set": {"favorite_categories": cats, "last_update": datetime.now()}},
                upsert=True
            )
            print("  ✓ Categorías actualizadas.")
        elif opt == "3":
            email = input("Email del usuario: ")
            user = db.users.find_one({"email": email})
            if not user:
                print("  Usuario no encontrado.")
                continue
            min_p = float(input("Precio mínimo: "))
            max_p = float(input("Precio máximo: "))
            db.user_preferences.update_one(
                {"user_id": user["_id"]},
                {"$set": {"price_range": {"min": min_p, "max": max_p}, "last_update": datetime.now()}},
                upsert=True
            )
            print("  ✓ Rango de precio actualizado.")
        elif opt == "9":
            print(f"\n  {RF_DESCRIPTIONS[5]}")
        elif opt == "0":
            break


# ==================== RF6: Índices para Optimización ====================

def rf6_create_indexes():
    print(f"\n  {RF_DESCRIPTIONS[6]}")
    db.users.create_index("email", unique=True)
    db.products.create_index([("category", 1), ("price", 1)])
    db.products.create_index([("name", "text")])
    db.carts.create_index("user_id")
    db.user_preferences.create_index("user_id")
    print("\n✓ Índices creados.")


# ==================== RF7: Pipeline de Agregación (Popularidad) ====================

def rf7_top_products():
    print(f"\n  {RF_DESCRIPTIONS[7]}")
    pipeline = [
        {"$match": {"cart_status": {"$in": ["active", "converted"]}}},
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.product_id",
            "total_count": {"$sum": "$items.quantity"},
            "product_name": {"$first": "$items.name"},
        }},
        {"$sort": {"total_count": -1}},
        {"$limit": 10},
    ]
    results = list(db.carts.aggregate(pipeline))
    if not results:
        print("  No hay datos para analizar.")
        return
    print("\n  Top 10 Productos Más Populares:")
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['product_name']} — {r['total_count']} unidades en carritos")
