
import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

load_dotenv(override=True)
MONGODB_URI = os.environ['MONGODB_URI']
DATABASE_NAME = os.environ['DATABASE_NAME']

def getDatabase():
    try:
        # Create a connection using MongoClient
        client = MongoClient(MONGODB_URI, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)
        # Attempt to connect
        client.server_info()
        
        # Create the database
        return client[DATABASE_NAME]
    except errors.ServerSelectionTimeoutError as err:
        print(f"Failed to connect to server: {err}")
        return None
    except errors.ConnectionFailure as err:
        print(f"Connection failed: {err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None
