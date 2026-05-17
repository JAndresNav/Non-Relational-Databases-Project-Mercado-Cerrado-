# Mercado Cerrado (Bases de datos no relacionales)

- José Andrés Navarro Ozuna 744998
- Maria Rebeca Armenta Armanta 759951
- Andrés Huerta Vasquez 759666

# Contexto del Proyecto: Mercado Cerrado

**Mercado Cerrado** es una plataforma de e-commerce diseñada para demostrar el uso eficiente de arquitecturas de bases de datos políglotas. En un entorno real, un solo motor de base de datos rara vez es óptimo para todas las necesidades. Por ello, hemos dividido el sistema en tres capas funcionales:

1.  **Capa de Negocio (MongoDB):** Gestiona el núcleo de la aplicación (catálogo, perfiles, carritos). Elegimos MongoDB por su flexibilidad para manejar datos semi-estructurados y su capacidad de escala horizontal para operaciones CRUD frecuentes.
2.  **Capa de Inteligencia y Relaciones (Dgraph):** Gestiona la red de interacciones entre usuarios y productos. Los grafos son ideales aquí porque permiten realizar recomendaciones complejas (filtrado colaborativo, co-compras) atravesando múltiples niveles de relación sin la penalización de rendimiento de los JOINs relacionales.
3.  **Capa de Observabilidad y Logs (Cassandra):** Registra el historial inmutable de actividad. Cassandra es perfecta para esta tarea debido a su altísima velocidad de escritura y su diseño orientado a consultas específicas (logs cronológicos), permitiendo auditorías y análisis de comportamiento a gran escala.

# Setup

## Python Environment

```bash
# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\Activate.ps1 # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Docker (Levantar servicios)

Para ejecutar el proyecto, es necesario tener los siguientes contenedores activos:

```bash
# MongoDB
docker run -d --name mongo-mercado -p 27017:27017 mongo:latest

# Dgraph (Standalone + Ratel UI)
docker run -d --name dgraph-mercado -p 8080:8080 -p 9080:9080 dgraph/standalone:latest
docker run -d --name ratel-mercado -p 8000:8000 dgraph/ratel:latest

# Cassandra
docker run -d --name cassandra-mercado -p 9042:9042 cassandra:latest
```

## Ejecutar

```bash
python main.py
```

# Flujo de Trabajo y Arquitectura

## MongoDB (Persistencia y Catálogo)

La interacción con MongoDB se centraliza en `connect.py` (usando un patrón Singleton para eficiencia de recursos) y la lógica de consultas en `Mongo/mongo.py`.

- **Optimización de Índices:** Se configuraron índices para cubrir patrones de consulta reales:
    - `email` (único): Búsqueda de usuarios.
    - `category + price`: Búsquedas filtradas por catálogo.
    - `name` (text): Búsquedas por palabras clave usando el motor de búsqueda de MongoDB.
    - `price`: Para rangos de precio eficientes.
- **Operación:** Se prioriza el uso de índices sobre escaneos de colección (Regex), mejorando drásticamente el rendimiento en catálogos grandes.

## Dgraph (Grafos y Recomendaciones)

Gestiona la inteligencia del sistema a través de relaciones semánticas. 

- **Modelo de Relaciones:** Se utilizan aristas directas como `bought` (compró) y `rated` (calificó) junto con relaciones a través de entidades intermedias para permitir consultas de recomendación potentes y flexibles.
- **Consultas de Grafos:** 
    - **RF1 (Filtrado Colaborativo):** Encuentra productos que otros usuarios compraron basándose en el historial del usuario actual (`bought -> ~bought -> bought`).
    - **RF4 (Co-compra):** Identifica qué productos se compran frecuentemente en la misma orden.

## Cassandra (Logs y Auditoría de Eventos)

Diseñada para el almacenamiento de series temporales de alta velocidad.

- **Diversidad de Partition Keys:** Hemos corregido el diseño inicial para evitar "Hot Spots". Ahora el esquema soporta múltiples patrones de acceso:
    - **Query por Usuario:** (`user_id` como PK) para ver el historial personal de un cliente.
    - **Query por Producto:** (`product_id` como PK) para analizar el tráfico o la evolución de precios de un artículo específico en toda la plataforma.
- **Clustering Keys:** Se utiliza el tiempo (`viewed_at`, `captured_at`) para mantener los datos ordenados físicamente en disco, permitiendo lecturas secuenciales extremadamente rápidas de los eventos más recientes.

# Estructura del Proyecto

```text
project-name/
├── Cassandra/    # Lógica de Cassandra y schema.cql (Diseño Query-First)
├── Mongo/        # Definición de esquemas, índices y consultas optimizadas
├── Dgraph/       # Esquema de grafos y lógica de recomendaciones transversales
├── data/         # Datasets en CSV para los tres motores
├── connect.py    # Gestión de conexiones (Singleton Pattern)
├── populate.py   # Script de carga masiva y gestión de esquema
├── main.py       # Interfaz de usuario (Menús)
└── README.md     # Documentación técnica y de negocio
```
