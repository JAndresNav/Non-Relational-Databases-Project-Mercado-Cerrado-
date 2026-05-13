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
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    
    if keyspace:
        try:
            session.set_keyspace(keyspace)
        except Exception:
            pass
    return session
