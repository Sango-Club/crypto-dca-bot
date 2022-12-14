import pymongo
from order import Order
from typing import List

class Database(pymongo.MongoClient):
    def __init__(self, mongourl: str, user: str, pwd: str, orders: List[Order]):
        host = f"mongodb+srv://{user}:{pwd}@{mongourl}/?retryWrites=true&w=majority"
        super().__init__(host)

        # Create empty collections