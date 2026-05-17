from pymongo import MongoClient
import pydgraph
from cassandra.cluster import Cluster
import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if DatabaseConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.mongo_client = None
            self.dgraph_client = None
            self.dgraph_stub = None
            self.cassandra_cluster = None
            self.cassandra_session = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = DatabaseConnection()
        return cls._instance

    def get_mongo_db(self):
        if self.mongo_client is None:
            self.mongo_client = MongoClient("mongodb://localhost:27017")
        return self.mongo_client["mercado_cerrado"]

    def get_dgraph_client(self):
        if self.dgraph_stub is None:
            self.dgraph_stub = pydgraph.DgraphClientStub('localhost:9080')
            self.dgraph_client = pydgraph.DgraphClient(self.dgraph_stub)
        return self.dgraph_client

    def get_cassandra_session(self, keyspace=None):
        if self.cassandra_cluster is None:
            self.cassandra_cluster = Cluster(['127.0.0.1'], port=9042)
            self.cassandra_session = self.cassandra_cluster.connect()
        
        if keyspace:
            try:
                self.cassandra_session.set_keyspace(keyspace)
            except Exception:
                pass
        return self.cassandra_session

    def close_all(self):
        if self.mongo_client:
            self.mongo_client.close()
            self.mongo_client = None
        if self.dgraph_stub:
            self.dgraph_stub.close()
            self.dgraph_stub = None
            self.dgraph_client = None
        if self.cassandra_cluster:
            self.cassandra_cluster.shutdown()
            self.cassandra_cluster = None
            self.cassandra_session = None

db_connection = DatabaseConnection.get_instance()

def get_dgraph_client():
    return db_connection.get_dgraph_client()

def get_mongo_db():
    return db_connection.get_mongo_db()

def get_cassandra_session(keyspace=None):
    return db_connection.get_cassandra_session(keyspace)

def close_connections():
    db_connection.close_all()
