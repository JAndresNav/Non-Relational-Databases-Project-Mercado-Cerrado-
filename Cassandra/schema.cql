-- Keyspace para los logs del sistema e-commerce
CREATE KEYSPACE IF NOT EXISTS mercado_cerrado_logs
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE mercado_cerrado_logs;

-- Eliminar tablas existentes para asegurar actualización de esquema
DROP TABLE IF EXISTS product_views_by_user;
DROP TABLE IF EXISTS product_views_by_product;
DROP TABLE IF EXISTS search_history_by_user;
DROP TABLE IF EXISTS purchase_history_by_user;
DROP TABLE IF EXISTS login_logs_by_user;
DROP TABLE IF EXISTS cart_activity_by_user;
DROP TABLE IF EXISTS user_price_history;
DROP TABLE IF EXISTS price_history_by_product;
DROP TABLE IF EXISTS favorite_activity_by_user;

-- 1. Registro de Vistas de Productos (RF1)
-- Consulta: Ver los últimos productos que un usuario ha visitado.
CREATE TABLE IF NOT EXISTS product_views_by_user (
    user_id UUID,
    viewed_at TIMESTAMP,
    product_id UUID,
    product_name TEXT,
    category TEXT,
    PRIMARY KEY ((user_id), viewed_at)
) WITH CLUSTERING ORDER BY (viewed_at DESC);

-- Consulta: Ver quién ha visitado un producto específico (Demostración de diferente Partition Key).
CREATE TABLE IF NOT EXISTS product_views_by_product (
    product_id UUID,
    viewed_at TIMESTAMP,
    user_id UUID,
    product_name TEXT,
    PRIMARY KEY ((product_id), viewed_at)
) WITH CLUSTERING ORDER BY (viewed_at DESC);

-- 2. Historial de Búsquedas (RF2)
-- Consulta: Ver qué términos ha buscado el usuario recientemente.
CREATE TABLE IF NOT EXISTS search_history_by_user (
    user_id UUID,
    searched_at TIMESTAMP,
    search_query TEXT,
    PRIMARY KEY ((user_id), searched_at)
) WITH CLUSTERING ORDER BY (searched_at DESC);

-- 3. Historial de Compras (RF3)
-- Consulta: Ver el historial de pedidos completados por el usuario.
CREATE TABLE IF NOT EXISTS purchase_history_by_user (
    user_id UUID,
    purchase_time TIMESTAMP,
    order_id UUID,
    product_names LIST<TEXT>,
    total_amount DECIMAL,
    status TEXT,
    PRIMARY KEY ((user_id), purchase_time)
) WITH CLUSTERING ORDER BY (purchase_time DESC);

-- 4. Logs de Inicio de Sesión (RF4)
-- Consulta: Rastrear accesos por seguridad.
CREATE TABLE IF NOT EXISTS login_logs_by_user (
    user_id UUID,
    logged_at TIMESTAMP,
    PRIMARY KEY ((user_id), logged_at)
) WITH CLUSTERING ORDER BY (logged_at DESC);

-- 5. Actividad del Carrito (RF5)
-- Consulta: Ver si el usuario agrega/quita productos frecuentemente.
CREATE TABLE IF NOT EXISTS cart_activity_by_user (
    user_id UUID,
    event_time TIMESTAMP,
    product_id UUID,
    action TEXT, -- 'ADD' o 'REMOVE'
    PRIMARY KEY ((user_id), event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- 6. Historial de Precios Observados (RF6)
-- Consulta: Analizar qué precio visualizó un usuario para un producto.
CREATE TABLE IF NOT EXISTS user_price_history (
    user_id UUID,
    product_id UUID,
    captured_at TIMESTAMP,
    price_seen DECIMAL,
    PRIMARY KEY ((user_id), product_id, captured_at)
) WITH CLUSTERING ORDER BY (product_id ASC, captured_at DESC);

-- Consulta: Ver la evolución del precio de un producto (Demostración de diferente Partition Key).
CREATE TABLE IF NOT EXISTS price_history_by_product (
    product_id UUID,
    captured_at TIMESTAMP,
    price_seen DECIMAL,
    PRIMARY KEY ((product_id), captured_at)
) WITH CLUSTERING ORDER BY (captured_at DESC);

-- 7. Registro de Favoritos (RF7)
-- Consulta: Ver cuándo un usuario marcó productos como favoritos.
CREATE TABLE IF NOT EXISTS favorite_activity_by_user (
    user_id UUID,
    added_at TIMESTAMP,
    product_id UUID,
    PRIMARY KEY ((user_id), added_at)
) WITH CLUSTERING ORDER BY (added_at DESC);
