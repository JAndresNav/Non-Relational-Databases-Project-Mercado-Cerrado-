import json
from connect import get_dgraph_client

client = get_dgraph_client()

def run_query(query):
    txn = client.txn()
    try:
        res = txn.query(query)
        data = json.loads(res.json)
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        txn.discard()

# ==================== RF1: Filtrado Colaborativo ====================
def rf1_menuD():
    while True:
        print("\n--- RF1: Filtrado Colaborativo ---")
        print("1. Buscar recomendaciones por Email")
        print("2. Buscar recomendaciones por Nombre")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        
        if opt == "1" or opt == "2":
            condicion = f'eq(email, "{input("Email del usuario: ")}")' if opt == "1" else f'eq(name, "{input("Nombre del usuario: ")}")'
            query = f"""
            {{
              rf1(func: {condicion}) {{
                name
                bought {{
                  name
                  ~bought {{
                    name
                    bought {{ name price }}
                  }}
                }}
              }}
            }}
            """
            run_query(query)
        elif opt == "0":
            break


# ==================== RF2: Reseñas como Nodos de Conexión ====================
def rf2_menuD():
    while True:
        print("\n--- RF2: Reseñas como Nodos de Conexión ---")
        print("1. Ver el historial de reseñas por Email")
        print("2. Ver el historial de reseñas por Nombre")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        
        if opt == "1" or opt == "2":
            condicion = f'eq(email, "{input("Email del usuario: ")}")' if opt == "1" else f'eq(name, "{input("Nombre del usuario: ")}")'
            query = f"""
            {{
              rf2(func: {condicion}) {{
                name
                wrote_review {{
                  rating
                  text
                  review_for {{ name price }}
                }}
              }}
            }}
            """
            run_query(query)
        elif opt == "0":
            break


# ================= RF3: Filtrado de Calidad y Clientes Frecuentes ============
def rf3_menuD():
    print("\n--- RF3: Filtrado de Calidad y Clientes Frecuentes ---")
    print("Obteniendo recomendaciones TOP de clientes frecuentes...")
    
    query = """
    {
      rf3(func: eq(is_frequent, true)) {
        name
        wrote_review @filter(ge(rating, 4)) {
          rating
          review_for { name price }
        }
      }
    }
    """
    run_query(query)


# ================ RF4: Productos Adquiridos Juntos (Co-compra) ===========
def rf4_menuD():
    while True:
        print("\n--- RF4: Productos Adquiridos Juntos (Co-compra) ---")
        print("1. Ver artículos comprados junto a un producto")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        if opt == "1":
            prod = input("Nombre del producto exacto: ")
            query = f"""
            {{
              rf4(func: eq(name, "{prod}")) {{
                name
                ~contains {{
                  ~placed {{
                    name
                    email
                    placed {{
                      contains {{
                        name
                        price
                      }}
                    }}
                  }}
                }}
              }}
            }}
            """
            run_query(query)
        elif opt == "0":
            break


# ==================== RF5: Grafo de Actividad del Usuario ====================
def rf5_menuD():
    while True:
        print("\n--- RF5: Grafo de Actividad del Usuario ---")
        print("1. Ver interacciones directas por Email")
        print("2. Ver interacciones directas por Nombre")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        
        if opt == "1" or opt == "2":
            cond = f'eq(email, "{input("Email del usuario: ")}")' if opt == "1" else f'eq(name, "{input("Nombre del usuario: ")}")'
            query = f"""
            {{
              rf5(func: {cond}) {{
                name
                bought {{ name price }}  # Cambiado 'purchased' por 'bought'
                rated {{ name price }}
              }}
            }}
            """
            run_query(query)
        elif opt == "0":
            break


# =============== RF6: Descubrimiento por Categoría Preferida ===============
def rf6_menuD():
    while True:
        print("\n--- RF6: Descubrimiento por Categoría Preferida ---")
        print("1. Analizar compras por categoría usando Email")
        print("2. Analizar compras por categoría usando Nombre")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        
        if opt == "1" or opt == "2":
            cond = f'eq(email, "{input("Email del usuario: ")}")' if opt == "1" else f'eq(name, "{input("Nombre del usuario: ")}")'
            query = f"""
            {{
              rf6(func: {cond}) {{
                name
                bought {{
                  name
                  belongs_to {{ category_name }}
                }}
              }}
            }}
            """
            run_query(query)
        elif opt == "0":
            break


# ============= RF7: Recomendación de Novedades por Compatibilidad ===========
def rf7_menuD():
    while True:
        print("\n--- RF7: Recomendación de Novedades por Compatibilidad ---")
        print("1. Recomendar productos nuevos por Email")
        print("2. Recomendar productos nuevos por Nombre")
        print("0. Regresar")
        opt = input("Selecciona una opción: ")
        
        if opt == "1" or opt == "2":
            cond = f'eq(email, "{input("Email del usuario: ")}")' if opt == "1" else f'eq(name, "{input("Nombre del usuario: ")}")'
            query = f"""
            {{
              rf7(func: {cond}) {{
                name
                bought {{
                  belongs_to {{
                    category_name
                    ~belongs_to @filter(eq(is_new, true)) {{ name price }}
                  }}
                }}
              }}
            }}
            """
            run_query(query)
        elif opt == "0":
            break       