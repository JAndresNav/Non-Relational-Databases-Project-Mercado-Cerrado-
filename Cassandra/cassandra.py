import uuid
from datetime import datetime
from connect import get_cassandra_session
from populate import populate_cassandra, drop_all_cassandra

def get_session():
    try:
        return get_cassandra_session("mercado_cerrado_logs")
    except Exception:
        return None

# ==================== RF1: Vistas de Productos ====================
def rf1_vistas_usuario():
    session = get_session()
    if not session: return
    print("1. Ver por Usuario (Partition Key: user_id)")
    print("2. Ver por Producto (Partition Key: product_id)")
    sub_opt = input("Selecciona sub-opción: ")
    
    if sub_opt == "1":
        user_id = input("UUID del usuario: ")
        query = "SELECT viewed_at, product_id, product_name, category FROM product_views_by_user WHERE user_id = %s"
        rows = session.execute(query, [uuid.UUID(user_id)])
        print("\n--- Historial de Vistas por Usuario ---")
        for row in rows:
            print(f"[{row.viewed_at}] Producto: {row.product_name} ({row.product_id}) | Cat: {row.category}")
    elif sub_opt == "2":
        prod_id = input("UUID del producto: ")
        query = "SELECT viewed_at, user_id, product_name FROM product_views_by_product WHERE product_id = %s"
        rows = session.execute(query, [uuid.UUID(prod_id)])
        print("\n--- Historial de Vistas por Producto ---")
        for row in rows:
            print(f"[{row.viewed_at}] Usuario: {row.user_id} | Nombre: {row.product_name}")

# ==================== RF2: Historial de Búsquedas ====================
def rf2_busquedas_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT searched_at, search_query FROM search_history_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Historial de Búsquedas ---")
    for row in rows:
        print(f"[{row.searched_at}] Término: '{row.search_query}'")

# ==================== RF3: Historial de Compras (List Type) ====================
def rf3_compras_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT purchase_time, order_id, product_names, total_amount, status FROM purchase_history_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Historial de Compras (Logs de Pedidos) ---")
    for row in rows:
        products = ", ".join(row.product_names)
        print(f"[{row.purchase_time}] Orden: {row.order_id} | Total: ${row.total_amount} | Status: {row.status}")
        print(f"    Productos: {products}")

# ==================== RF4: Logs de Login ====================
def rf4_logins_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT logged_at FROM login_logs_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Logs de Inicio de Sesión ---")
    for row in rows:
        print(f"[{row.logged_at}] Sesión iniciada")

# ==================== RF5: Actividad del Carrito ====================
def rf5_actividad_carrito():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT event_time, action, product_id FROM cart_activity_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Actividad del Carrito ---")
    for row in rows:
        print(f"[{row.event_time}] Acción: {row.action} | Producto: {row.product_id}")

# ==================== RF6: Historial de Precios Observados ====================
def rf6_cambios_precio():
    session = get_session()
    if not session: return
    print("1. Ver por Usuario y Producto (PK: user_id, product_id)")
    print("2. Ver evolución por Producto (PK: product_id)")
    sub_opt = input("Selecciona sub-opción: ")

    if sub_opt == "1":
        user_id = input("UUID del usuario: ")
        product_id = input("UUID del producto: ")
        query = "SELECT captured_at, price_seen FROM user_price_history WHERE user_id = %s AND product_id = %s"
        rows = session.execute(query, [uuid.UUID(user_id), uuid.UUID(product_id)])
        print("\n--- Precios Visualizados por el Usuario ---")
        for row in rows:
            print(f"[{row.captured_at}] Precio observado: ${row.price_seen}")
    elif sub_opt == "2":
        product_id = input("UUID del producto: ")
        query = "SELECT captured_at, price_seen FROM price_history_by_product WHERE product_id = %s"
        rows = session.execute(query, [uuid.UUID(product_id)])
        print("\n--- Evolución de Precios del Producto ---")
        for row in rows:
            print(f"[{row.captured_at}] Precio: ${row.price_seen}")

# ==================== RF7: Registro de Favoritos ====================
def rf7_favoritos_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT added_at, product_id FROM favorite_activity_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Registro de Favoritos ---")
    for row in rows:
        print(f"[{row.added_at}] Producto: {row.product_id}")
