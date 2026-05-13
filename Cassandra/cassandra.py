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
    user_id = input("UUID del usuario: ")
    query = "SELECT view_timestamp, product_id, category, price FROM product_views_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Historial de Vistas ---")
    for row in rows:
        print(f"[{row.view_timestamp}] Producto: {row.product_id} | Cat: {row.category} | ${row.price}")

# ==================== RF2: Historial de Búsquedas ====================
def rf2_busquedas_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT search_timestamp, query, results_count FROM search_history_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Historial de Búsquedas ---")
    for row in rows:
        print(f"[{row.search_timestamp}] Término: '{row.query}' | Resultados: {row.results_count}")

# ==================== RF3: Historial de Compras (List Type) ====================
def rf3_compras_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT purchase_timestamp, order_id, product_names, total_amount FROM purchase_history_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Historial de Compras (Logs de Pedidos) ---")
    for row in rows:
        products = ", ".join(row.product_names)
        print(f"[{row.purchase_timestamp}] Orden: {row.order_id} | Total: ${row.total_amount}")
        print(f"    Productos: {products}")

# ==================== RF4: Logs de Login ====================
def rf4_logins_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT login_timestamp, ip_address, device FROM login_logs_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Logs de Inicio de Sesión ---")
    for row in rows:
        print(f"[{row.login_timestamp}] IP: {row.ip_address} | Dispositivo: {row.device}")

# ==================== RF5: Actividad del Carrito ====================
def rf5_actividad_carrito():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT activity_timestamp, action, product_id, quantity FROM cart_activity_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Actividad del Carrito ---")
    for row in rows:
        print(f"[{row.activity_timestamp}] Acción: {row.action} | Producto: {row.product_id} | Cant: {row.quantity}")

# ==================== RF6: Cambios de Precio ====================
def rf6_cambios_precio():
    session = get_session()
    if not session: return
    product_id = input("UUID del producto: ")
    query = "SELECT change_timestamp, old_price, new_price, discount_pct FROM price_changes_by_product WHERE product_id = %s"
    rows = session.execute(query, [uuid.UUID(product_id)])
    print("\n--- Histórico de Precios del Producto ---")
    for row in rows:
        print(f"[{row.change_timestamp}] {row.old_price} -> {row.new_price} (Dcto: {row.discount_pct}%)")

# ==================== RF7: Registro de Favoritos ====================
def rf7_favoritos_usuario():
    session = get_session()
    if not session: return
    user_id = input("UUID del usuario: ")
    query = "SELECT fav_timestamp, product_id, note FROM favorite_activity_by_user WHERE user_id = %s"
    rows = session.execute(query, [uuid.UUID(user_id)])
    print("\n--- Registro de Favoritos ---")
    for row in rows:
        print(f"[{row.fav_timestamp}] Producto: {row.product_id} | Nota: {row.note}")
