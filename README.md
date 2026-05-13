# Mercado Cerrado (Bases de datos no relacionales)

- José Andrés Navarro Ozuna 744998
- Maria Rebeca Armenta Armanta 759951
- Andrés Huerta Vasquez 759666

# Descripción del proyecto

Este proyecto desarrolla un Sistema de Recomendaciones para E-Commerce que personaliza la experiencia de compra mediante el análisis del comportamiento de los usuarios, sus preferencias y las interacciones con productos. El sistema integra múltiples bases de datos no relacionales: MongoDB para el almacenamiento de productos, usuarios y carritos; Dgraph para gestionar relaciones y generar recomendaciones basadas en afinidad y reseñas; y Cassandra para registrar actividades y eventos del usuario. El objetivo es mejorar la búsqueda de productos, optimizar el inventario y ofrecer recomendaciones relevantes que faciliten la toma de decisiones y aumenten la eficiencia de la plataforma.

# Setup

## Python Environment

```bash
python -m venv venv

# Windows
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Docker

```bash
docker run -d --name mongo-mercado -p 27017:27017 mongo:latest
```
```bash
docker run -d --name dgraph-mercado -p 8080:8080 -p 9080:9080 dgraph/standalone:latest
```
```bash
docker run --name ratel-mercado -d -p 8000:8000 dgraph/ratel:latest
```
```bash
docker run -d --name cassandra-mercado -p 9042:9042 cassandra:latest
```

## Ejecutar

```bash
python main.py
```

# Flujo de Trabajo

## MongoDB

La interacción con MongoDB se centraliza en `connect.py` utilizando la librería `pymongo`. La lógica se encuentra en `Mongo/mongo.py`.

- **Conexión:** `connect.py` establece la conexión al contenedor Docker en `localhost:27017`, base de datos `mercado_cerrado`.
- **Población:** Desde el menú, la opción "Populate" ejecuta `populate()` que crea y pobla todas las colecciones (products, users, carts, wishlists, user_preferences).
- **Índices:** Índice único en `users.email`, compuesto en `products.category+price`, texto en `products.name`, e índices en `carts.user_id` y `user_preferences.user_id`.
- **Consultas:** Cada opción RF1–RF7 del submenú MongoDB ejecuta funciones en `Mongo/mongo.py`.

## Dgraph

En Dgraph, la conexión se establece desde connect.py utilizando el cliente oficial pydgraph en Python.

## Cassandra

El registro de logs y auditoría se gestiona mediante el driver `cassandra-driver` en `connect.py`.

- **Esquema:** Ubicado en `Cassandra/schema.cql`. Implementa un diseño **"Query-First"** con 7 tablas de logs (vistas, búsquedas, compras, logins, carritos, precios y favoritos). Las tablas utilizan particiones por ID y clustering keys cronológicas para optimizar la velocidad de lectura.
- **Operación:** `populate.py` contiene la lógica `populate_cassandra()` para la creación automática del esquema e ingesta de datos desde archivos CSV en `data/Cassandra/`.
- **Consultas:** El módulo `Cassandra/cassandra.py` centraliza el menú de Cassandra y las consultas para recuperar los distintos tipos de logs de actividad.

# Estructura del Proyecto

```text
project-name/
├── Cassandra/    # Lógica de Cassandra y schema.cql
├── Mongo/        # Definición de esquemas e índices
├── Dgraph/       # Esquema de predicados y tipos
├── data/         # Archivos fuente (CSVs por motor)
│   ├── Mongo/
│   ├── Dgraph/
│   └── Cassandra/
├── connect.py    # Gestión de conexiones a las 3 BD
├── populate.py   # Plan detallado de población de datos
├── main.py       # Menú de consultas funcionales
└── README.md     # Documentación del proyecto
```
