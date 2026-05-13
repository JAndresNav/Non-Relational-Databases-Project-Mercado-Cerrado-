from pymongo import MongoClient
import pydgraph
from cassandra.cluster import Cluster

def get_dgraph_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    return pydgraph.DgraphClient(client_stub)

def get_mongo_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["mercado_cerrado"]

def get_cassandra_session(keyspace='mercado_cerrado_logs'):
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()
    
    try:
        session.set_keyspace(keyspace)
    except Exception as e:
        print(f"El Keyspace '{keyspace}' no existe o no se pudo conectar: {e}")
        print("Recuerda crearlo en cqlsh primero.")
        
    return session
