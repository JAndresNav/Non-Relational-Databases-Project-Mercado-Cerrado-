-- Keyspace para los logs del sistema e-commerce
CREATE KEYSPACE IF NOT EXISTS mercado_cerrado_logs
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE mercado_cerrado_logs;

-- 1. Registro de Vistas de Productos
-- Consulta: Ver los últimos productos que un usuario ha visitado.
CREATE TABLE IF NOT EXISTS product_views_by_user (
    user_id UUID,
    view_timestamp TIMESTAMP,
    product_id UUID,
    category TEXT,
    price DECIMAL,
    PRIMARY KEY ((user_id), view_timestamp)
) WITH CLUSTERING ORDER BY (view_timestamp DESC);

-- 2. Historial de Búsquedas
-- Consulta: Ver qué términos ha buscado el usuario recientemente.
CREATE TABLE IF NOT EXISTS search_history_by_user (
    user_id UUID,
    search_timestamp TIMESTAMP,
    query TEXT,
    results_count INT,
    PRIMARY KEY ((user_id), search_timestamp)
) WITH CLUSTERING ORDER BY (search_timestamp DESC);

-- 3. Historial de Compras (RF3)
-- Consulta: Ver el historial de pedidos completados por el usuario.
CREATE TABLE IF NOT EXISTS purchase_history_by_user (
    user_id UUID,
    purchase_timestamp TIMESTAMP,
    order_id UUID,
    -- Se usa LIST en lugar de SET para permitir productos duplicados en un mismo ticket
    -- y mantener el orden de inserción de los artículos (orden del carrito).
    product_names LIST<TEXT>,
    total_amount DECIMAL,
    PRIMARY KEY ((user_id), purchase_timestamp)
) WITH CLUSTERING ORDER BY (purchase_timestamp DESC);

-- 4. Logs de Inicio de Sesión
-- Consulta: Rastrear accesos por seguridad y ubicación.
CREATE TABLE IF NOT EXISTS login_logs_by_user (
    user_id UUID,
    login_timestamp TIMESTAMP,
    ip_address TEXT,
    device TEXT,
    PRIMARY KEY ((user_id), login_timestamp)
) WITH CLUSTERING ORDER BY (login_timestamp DESC);

-- 5. Actividad del Carrito (Logs de eventos)
-- Consulta: Ver si el usuario agrega/quita productos frecuentemente.
CREATE TABLE IF NOT EXISTS cart_activity_by_user (
    user_id UUID,
    activity_timestamp TIMESTAMP,
    action TEXT, -- 'ADD' o 'REMOVE'
    product_id UUID,
    quantity INT,
    PRIMARY KEY ((user_id), activity_timestamp)
) WITH CLUSTERING ORDER BY (activity_timestamp DESC);

-- 6. Alertas/Cambios de Precio
-- Consulta: Ver el histórico de precios de un producto específico.
CREATE TABLE IF NOT EXISTS price_changes_by_product (
    product_id UUID,
    change_timestamp TIMESTAMP,
    old_price DECIMAL,
    new_price DECIMAL,
    discount_pct FLOAT,
    PRIMARY KEY ((product_id), change_timestamp)
) WITH CLUSTERING ORDER BY (change_timestamp DESC);

-- 7. Registro de Favoritos (Añadidos)
-- Consulta: Ver cuándo un usuario marcó productos como favoritos.
CREATE TABLE IF NOT EXISTS favorite_activity_by_user (
    user_id UUID,
    fav_timestamp TIMESTAMP,
    product_id UUID,
    note TEXT,
    PRIMARY KEY ((user_id), fav_timestamp)
) WITH CLUSTERING ORDER BY (fav_timestamp DESC);
