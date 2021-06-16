"""
Create database and collection before insert to data lake,
In case we use mongoDB.

"""
from constants import CLIENT, DATABASE, COLLECTION

import pymongo


class MongoDB():

    def __init__(self, client=None, database=None, collection=None):
        # create class constructor
        self.client = pymongo.MongoClient(CLIENT)
        self.database = DATABASE
        self.collection = COLLECTION

    def create_database(self):
        dblist = self.client.list_database_names()
        print('dblist : {}'.format(dblist))
        if self.database not in dblist:
            stock_db = self.client[self.database]
            print("The database stock_price was created.")

    def create_collection(self):
        collist = self.client[self.database].list_collection_names()
        if self.collection not in collist:
            set_col = self.client[self.database]["set_index"]
            print("The collection set_index was created.")

    def insert_one(self, data):
        """
        Insert data to collection

        Args:
        data(list) : list of dict

        Return:
        list of object id
        """
        _client = self.client
        _db = _client[self.database]
        _col = _db[self.collection]

        x = _col.insert_one(data)

        return x


if __name__ == "__main__":
    mongo = MongoDB()
    mongo.create_database()
