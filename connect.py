from pymongo import MongoClient
import pydgraph

def get_dgraph_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    return pydgraph.DgraphClient(client_stub)

def get_mongo_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["mercado_cerrado"]
