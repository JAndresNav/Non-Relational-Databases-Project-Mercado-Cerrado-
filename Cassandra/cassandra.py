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
    print("1. Ver por Usuario (PK: user_id, Event: VIEW)")
    print("2. Ver por Producto (PK: product_id, Event: VIEW)")
    sub_opt = input("Selecciona sub-opción: ")
    
    if sub_opt == "1":
        user_id = input("UUID del usuario: ")
        query = "SELECT event_time, product_id, product_name, category FROM activity_by_user WHERE user_id = %s AND event_type = 'VIEW'"
        rows = session.execute(query, [uuid.UUID(user_id)])
        print("\n--- Historial de Vistas por Usuario ---")
        for row in rows:
            print(f"[{row.event_time}] Producto: {row.product_name} ({row.product_id}) | Cat: {row.category}")
    elif sub_opt == "2":
        prod_id = input("UUID del producto: ")
        query = "SELECT event_time, user_id, product_name FROM activity_by_product WHERE product_id = %s AND event_type = 'VIEW'"
        rows = session.execute(query, [uuid.UUID(prod_id)])
        print("\n--- Historial de Vistas por Producto ---")
        for row in rows:
            print(f"[{row.event_time}] Usuario: {row.user_id} | Nombre: {row.product_name}")

# ==================== RF2: Historial de Búsquedas ====================
def rf2_busquedas_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT event_time, search_query FROM activity_by_user WHERE user_id = %s AND event_type = 'SEARCH'"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Historial de Búsquedas ---")
    for row in rows:
        print(f"[{row.event_time}] Término: '{row.search_query}'")

# ==================== RF3: Historial de Compras ====================
def rf3_compras_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT event_time, order_id, total_amount, status FROM activity_by_user WHERE user_id = %s AND event_type = 'PURCHASE'"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Historial de Compras (Logs de Pedidos) ---")
    for row in rows:
        print(f"[{row.event_time}] Orden: {row.order_id} | Total: ${row.total_amount} | Status: {row.status}")

# ==================== RF4: Logs de Login ====================
def rf4_logins_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT event_time FROM activity_by_user WHERE user_id = %s AND event_type = 'LOGIN'"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Logs de Inicio de Sesión ---")
    for row in rows:
        print(f"[{row.event_time}] Sesión iniciada")

# ==================== RF5: Actividad del Carrito ====================
def rf5_actividad_carrito():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT event_time, action, product_id FROM activity_by_user WHERE user_id = %s AND event_type = 'CART'"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Actividad del Carrito ---")
    for row in rows:
        print(f"[{row.event_time}] Acción: {row.action} | Producto: {row.product_id}")

# ==================== RF6: Historial de Precios ====================
def rf6_cambios_precio():
    session = get_session()
    if not session: return
    print("1. Ver por Usuario y Producto (PK: user_id, Event: PRICE_WATCH)")
    print("2. Ver evolución por Producto (PK: product_id, Event: PRICE_HISTORY)")
    sub_opt = input("Selecciona sub-opción: ")

    if sub_opt == "1":
        user_id = input("UUID del usuario: ")
        query = "SELECT event_time, product_id, price_seen FROM activity_by_user WHERE user_id = %s AND event_type = 'PRICE_WATCH'"
        rows = session.execute(query, [uuid.UUID(user_id)])
        print("\n--- Precios Visualizados por el Usuario ---")
        for row in rows:
            print(f"[{row.event_time}] Producto: {row.product_id} | Precio observado: ${row.price_seen}")
    elif sub_opt == "2":
        product_id = input("UUID del producto: ")
        query = "SELECT event_time, price_seen FROM activity_by_product WHERE product_id = %s AND event_type = 'PRICE_HISTORY'"
        rows = session.execute(query, [uuid.UUID(product_id)])
        print("\n--- Evolución de Precios del Producto ---")
        for row in rows:
            print(f"[{row.event_time}] Precio: ${row.price_seen}")

# ==================== RF7: Registro de Favoritos ====================
def rf7_favoritos_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT event_time, product_id FROM activity_by_user WHERE user_id = %s AND event_type = 'FAVORITE'"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Registro de Favoritos ---")
    for row in rows:
        print(f"[{row.event_time}] Producto: {row.product_id}")
