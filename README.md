# Mercado Cerrado (Bases de datos no relacionales)

- José Andrés Navarro Ozuna 744998
- Maria Rebeca Armenta Armanta 759951
- Andrés Huerta Vasquez 759666

# Descripción del proyecto

Este proyecto desarrolla un Sistema de Recomendaciones para E-Commerce que personaliza la experiencia de compra mediante el análisis del comportamiento de los usuarios, sus preferencias y las interacciones con productos. El sistema integra múltiples bases de datos no relacionales: MongoDB para el almacenamiento de productos, usuarios y carritos; Dgraph para gestionar relaciones y generar recomendaciones basadas en afinidad y reseñas; y Cassandra para registrar actividades y eventos del usuario. El objetivo es mejorar la búsqueda de productos, optimizar el inventario y ofrecer recomendaciones relevantes que faciliten la toma de decisiones y aumenten la eficiencia de la plataforma.

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

La interacción con MongoDB se centraliza en `connect.py` y la lógica de consultas en `Mongo/mongo.py`. Se eligió por su flexibilidad de esquema para manejar documentos anidados como direcciones y atributos variables de productos.

- **Diseño de Colecciones:** Implementa un modelo de datos orientado a documentos para `products`, `users`, `carts`, `wishlists` y `user_preferences`.
- **Optimización:** Se configuraron índices específicos para garantizar el rendimiento:
    - Índice único en `users.email` para evitar duplicidad.
    - Índice compuesto en `products.category + price` para búsquedas filtradas rápidas.
    - Índice de texto en `products.name` para búsquedas parciales.
- **Operación:** La función `populate_mongo()` se encarga de la limpieza de colecciones y carga de datos maestros, vinculando carritos y wishlists mediante `ObjectId` de usuario.

## Dgraph (Grafos y Recomendaciones)

Gestiona la inteligencia del sistema a través de relaciones complejas. Permite realizar recomendaciones que serían costosas en bases de datos relacionales o documentales.

- **Modelo de Grafos:** Define un esquema de predicados indexados para nodos tipo `User`, `Product`, `Category`, `Review` y `Order`.
- **Lógica de Relaciones:** Utiliza aristas (`edges`) como `bought`, `wrote_review`, `belongs_to` y `placed` para conectar usuarios con productos y órdenes.
- **Consultas (RF):** Implementa algoritmos de filtrado colaborativo (usuarios que compraron lo mismo), análisis de co-compra y descubrimiento de productos basado en la profundidad del grafo de actividad del usuario.

## Cassandra (Logs y Auditoría de Eventos)

Se encarga del registro masivo de eventos inmutables, aprovechando su alta capacidad de escritura y escalabilidad lineal.

- **Diseño Query-First:** El esquema en `Cassandra/schema.cql` está diseñado para responder a las consultas de logs sin realizar uniones.
    - Utiliza `user_id` como *Partition Key* para asegurar que los logs de un mismo usuario vivan en el mismo nodo.
    - Utiliza `timestamp` como *Clustering Key* con ordenamiento descendente para recuperar la actividad reciente de forma inmediata.
- **Estructuras Avanzadas:** 
    - Implementa `LIST<TEXT>` para el historial de compras, permitiendo registrar duplicados y mantener el orden del ticket de compra.
- **Automatización:** La carga de datos en `populate.py` crea automáticamente el Keyspace y las tablas leyendo el archivo CQL antes de procesar los CSVs de actividad.

# Estructura del Proyecto

```text
project-name/
├── Cassandra/    # Lógica de Cassandra y schema.cql
├── Mongo/        # Definición de esquemas, índices y consultas RF
├── Dgraph/       # Esquema de predicados, tipos y lógica de grafos
├── data/         # Archivos fuente (CSVs de carga inicial)
│   ├── Mongo/
│   ├── Dgraph/
│   └── Cassandra/
├── connect.py    # Gestión de conexiones políglotas
├── populate.py   # Script automatizado de población (Seeders)
├── main.py       # Interfaz de usuario y orquestador de menús
└── README.md     # Documentación del proyecto
```
