
import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors, server_api

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

def getDatabase():
    try:
        # Create a connection using MongoClient
        client = MongoClient(MONGODB_URI, server_api=server_api('1'))
        # Attempt to connect
        client.server_info()
        
        # Create the database
        return client['webir']
    except errors.ServerSelectionTimeoutError as err:
        print(f"Failed to connect to server: {err}")
        return None
    except errors.ConnectionFailure as err:
        print(f"Connection failed: {err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None


