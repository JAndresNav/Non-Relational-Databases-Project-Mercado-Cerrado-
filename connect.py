from pymongo import MongoClient
import pydgraph
from cassandra.cluster import Cluster

def get_dgraph_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    return pydgraph.DgraphClient(client_stub)

def get_mongo_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["mercado_cerrado"]

def get_cassandra_session(keyspace=None):
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()
    
    if keyspace:
        try:
            session.set_keyspace(keyspace)
        except Exception:
            # Si el keyspace no existe, no hacemos nada. 
            # Esto permite que populate cree el esquema.
            pass
            
    return session
