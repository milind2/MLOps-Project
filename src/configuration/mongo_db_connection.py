import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.
    """

    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if not mongo_db_url:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set.")

                # FIX: Added timeouts to prevent connection hang on broken shard
                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    tlsCAFile=ca,
                    connectTimeoutMS=10000,
                    serverSelectionTimeoutMS=10000,
                    socketTimeoutMS=10000
                )

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful.")

        except Exception as e:
            raise MyException(e, sys)
