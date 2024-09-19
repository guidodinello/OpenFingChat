import logging

from pymongo import MongoClient

import constants


def get_database():
    logging.info(
        "Connecting to database: %s. URI=%s",
        constants.DATABASE_NAME,
        constants.MONGODB_URI,
    )
    client = MongoClient(constants.MONGODB_URI)
    # Attempt to connect
    client.server_info()

    # Create the database
    return client[constants.DATABASE_NAME]
