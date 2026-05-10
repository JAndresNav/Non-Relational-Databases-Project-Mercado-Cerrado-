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
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## MongoDB (Docker)
```bash
docker run -d --name mongo-mercado -p 27017:27017 mongo:7
```

## Ejecutar
```bash
python main.py
```

# Flujo de Trabajo

## MongoDB

La interacción con MongoDB se centraliza en `connect.py` utilizando la librería `pymongo`. La lógica se encuentra en `Mongo/mongo.py`.
* **Conexión:** `connect.py` establece la conexión al contenedor Docker en `localhost:27017`, base de datos `mercado_cerrado`.
* **Población:** Desde el menú, la opción "Populate" ejecuta `populate()` que crea y pobla todas las colecciones (products, users, carts, wishlists, user_preferences).
* **Índices:** Índice único en `users.email`, compuesto en `products.category+price`, texto en `products.name`, e índices en `carts.user_id` y `user_preferences.user_id`.
* **Consultas:** Cada opción RF1–RF7 del submenú MongoDB ejecuta funciones en `Mongo/mongo.py`.

## Dgraph

En Dgraph, la conexión se establece desde connect.py utilizando el cliente oficial pydgraph en Python.
Dentro de la carpeta Dgraph/ se define el schema con los predicados y sus índices, el cual se aplica al iniciar la conexión mediante client.alter(). La inserción de datos en populate.py se realiza a través de transacciones (txn = client.txn()) que ejecutan mutaciones en formato JSON con txn.mutate(set_obj=data): primero se crean los nodos User, Product y Category, luego se establecen las aristas como bought, belongs_to y placed/contains al registrar órdenes, y finalmente se crean los nodos Review con sus aristas wrote_review y review_for.
Las consultas en main.py se ejecutan mediante DQL usando la terminal, donde cada opción del menú corresponde a un requerimiento funcional

## Cassandra

El registro de logs masivos se gestiona mediante el driver `cassandra-driver` en `connect.py`.
* **Esquema:** En la carpeta `Cassandra/` se encuentran los scripts `.cql` para la creación de las 7 tablas de actividad (vistas, búsquedas, logins, historial de precios, etc.). Se utiliza un diseño de "Query-First", donde la partición por `user_id` y el ordenamiento por clustering keys permiten lecturas de alta velocidad.
* **Operación:** `populate.py` contiene la lógica para la ingesta de eventos masivos. La lectura en `main.py` recupera historiales cronológicos y eventos de interacción con el carrito sin necesidad de procesos de unión de tablas, aprovechando la arquitectura de columnas de Cassandra.

## Estructura del Proyecto
```text
project-name/
├── Cassandra/    # Scripts de creación de tablas (.cql)
├── Mongo/        # Definición de esquemas e índices
├── Dgraph/       # Esquema de predicados y tipos
├── data/         # Archivos fuente (JSON/CSV)
├── connect.py    # Gestión de conexiones a las 3 BD
├── populate.py   # Plan detallado de población de datos
├── main.py       # Menú de consultas funcionales
└── README.md     # Documentación del proyecto
