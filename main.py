from populate import populate_mongo, drop_all_mongo, populate_dgraph, drop_all_dgraph
from Mongo.mongo import rf1_menu, rf2_menu, rf3_menu, rf4_menu, rf5_menu, rf6_create_indexes, rf7_top_products
from Dgraph.dgraph import rf1_menuD, rf2_menuD, rf3_menuD, rf4_menuD, rf4_menuD, rf5_menuD, rf6_menuD, rf7_menuD
from Cassandra.cassandra import cassandra_menu

def mongo_menu():
    while True:
        print("\n--- MongoDB ---")
        print("1. Populate (crear y poblar colecciones)")
        print("2. Drop All (eliminar colecciones)")
        print("3. RF1 - Catálogo de Productos")
        print("4. RF2 - Perfil General del Usuario")
        print("5. RF3 - Carrito de Compras Activo")
        print("6. RF4 - Lista de Deseos (Wishlist)")
        print("7. RF5 - Preferencias del Usuario")
        print("8. RF6 - Crear Índices")
        print("9. RF7 - Top 10 Productos Populares")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        if opt == "1":
            populate_mongo()
        elif opt == "2":
            drop_all_mongo()
        elif opt == "3":
            rf1_menu()
        elif opt == "4":
            rf2_menu()
        elif opt == "5":
            rf3_menu()
        elif opt == "6":
            rf4_menu()
        elif opt == "7":
            rf5_menu()
        elif opt == "8":
            rf6_create_indexes()
        elif opt == "9":
            rf7_top_products()
        elif opt == "0":
            break

def dgraph_menu():
    while True:
        print("\n--- Dgraph ---")
        print("1. Populate (crear esquema y poblar nodos/aristas)")
        print("2. Drop All (eliminar todo el grafo)")
        print("3. RF1 - Recomendaciones por Filtrado Colaborativo")
        print("4. RF2 - Reseñas como Nodos de Conexión")
        print("5. RF3 - Filtrado de Calidad y Clientes Frecuentes")
        print("6. RF4 - Productos Adquiridos Juntos (Co-compra)")
        print("7. RF5 - Grafo de Actividad del Usuario")
        print("8. RF6 - Descubrimiento por Categoría Preferida")
        print("9. RF7 - Recomendación por Compatibilidad")
        print("0. Regresar")
        
        opt = input("Selecciona una opción: ")
        
        if opt == "1":
            populate_dgraph()
        elif opt == "2":
            drop_all_dgraph()
        elif opt == "3":
            rf1_menuD()
        elif opt == "4":
            rf2_menuD()
        elif opt == "5":
            rf3_menuD()
        elif opt == "6":
            rf4_menuD()
        elif opt == "7":
            rf5_menuD()
        elif opt == "8":
            rf6_menuD()
        elif opt == "9":
            rf7_menuD()
        elif opt == "0":
            break


def main_menu():
    while True:
        print("\n=== Mercado Cerrado ===")
        print("1. MongoDB")
        print("2. Dgraph")
        print("3. Cassandra")
        print("0. Salir")
        opt = input("Selecciona una opción: ")
        if opt == "1":
            mongo_menu()
        elif opt == "2":
            dgraph_menu()
        elif opt == "3":
            cassandra_menu()
        elif opt == "0":
            break


if __name__ == "__main__":
    main_menu()
