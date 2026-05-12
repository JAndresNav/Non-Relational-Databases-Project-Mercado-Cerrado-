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
        print(f"Error en la consulta: {e}")
    finally:
        txn.discard()

        