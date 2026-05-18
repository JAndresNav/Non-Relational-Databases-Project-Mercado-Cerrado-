-- Keyspace para los logs del sistema e-commerce
CREATE KEYSPACE IF NOT EXISTS mercado_cerrado_logs
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE mercado_cerrado_logs;

-- Limpiar esquema anterior
DROP TABLE IF EXISTS activity_by_user;
DROP TABLE IF EXISTS activity_by_product;

-- 1. Tabla Unificada por Usuario
-- Soporta: RF1, RF2, RF3, RF4, RF5, RF6, RF7
CREATE TABLE IF NOT EXISTS activity_by_user (
    user_id UUID,
    event_type TEXT, -- 'VIEW', 'SEARCH', 'PURCHASE', 'LOGIN', 'CART', 'FAVORITE', 'PRICE_WATCH'
    event_time TIMESTAMP,
    product_id UUID,
    product_name TEXT,
    category TEXT,
    search_query TEXT,
    order_id UUID,
    total_amount DECIMAL,
    status TEXT,
    action TEXT, -- 'ADD', 'REMOVE'
    price_seen DECIMAL,
    PRIMARY KEY ((user_id), event_type, event_time)
) WITH CLUSTERING ORDER BY (event_type ASC, event_time DESC);

-- 2. Tabla Unificada por Producto (Para análisis de inventario y precios)
-- Soporta: RF1 (vistas por producto), RF6 (evolución de precios)
CREATE TABLE IF NOT EXISTS activity_by_product (
    product_id UUID,
    event_type TEXT, -- 'VIEW', 'PRICE_CHANGE'
    event_time TIMESTAMP,
    user_id UUID,
    product_name TEXT,
    price_seen DECIMAL,
    PRIMARY KEY ((product_id), event_type, event_time)
) WITH CLUSTERING ORDER BY (event_type ASC, event_time DESC);
