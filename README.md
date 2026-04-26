# Mercado Cerrado (Bases de datos no relacionales)

- José Andrés Navarro Ozuna 744998
- Maria Rebeca Armenta Armanta 759951
- Andrés Huerta Vasquez 759666

# Descripción del proyecto

Este proyecto desarrolla un Sistema de Recomendaciones para E-Commerce que personaliza la experiencia de compra mediante el análisis del comportamiento de los usuarios, sus preferencias y las interacciones con productos. El sistema integra múltiples bases de datos no relacionales: MongoDB para el almacenamiento de productos, usuarios y carritos; Dgraph para gestionar relaciones y generar recomendaciones basadas en afinidad y reseñas; y Cassandra para registrar actividades y eventos del usuario. El objetivo es mejorar la búsqueda de productos, optimizar el inventario y ofrecer recomendaciones relevantes que faciliten la toma de decisiones y aumenten la eficiencia de la plataforma.

# Flujo de Trabajo

## MongoDB

## Dgraph

En Dgraph, la conexión se establece desde connect.py utilizando el cliente oficial pydgraph en Python.
Dentro de la carpeta Dgraph/ se define el schema con los predicados y sus índices, el cual se aplica al iniciar la conexión mediante client.alter(). La inserción de datos en populate.py se realiza a través de transacciones (txn = client.txn()) que ejecutan mutaciones en formato JSON con txn.mutate(set_obj=data): primero se crean los nodos User, Product y Category, luego se establecen las aristas como bought, belongs_to y placed/contains al registrar órdenes, y finalmente se crean los nodos Review con sus aristas wrote_review y review_for.
Las consultas en main.py se ejecutan mediante DQL usando la terminal, donde cada opción del menú corresponde a un requerimiento funcional

## Cassandra
