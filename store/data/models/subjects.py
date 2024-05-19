from bson import ObjectId
from pymongo import errors
from store.data.connection import getDatabase

class SubjectModel:

    def __init__(self):
        try:
            db = getDatabase()
            self.collection = db['subjects']
        except ConnectionError as err:
            raise RuntimeError(f"Initialization failed: {err}")
        
    def get(self, subjectId):
        try:
            subject = self.collection.find_one({"_id": ObjectId(subjectId)})
            return subject
        except errors.PyMongoError as err:
            print(f"An error occurred while retrieving the subject: {err}")
            return None

    def getAll(self):       
        try:
            subjects = self.collection.find()
            return list(subjects)
        except errors.PyMongoError as err:
            print(f"An error occurred while retrieving all subjects: {err}")
            return []
        
    def create(self, name, url):
        try:
            result = self.collection.insert_one({ name, url })
            return result.inserted_id
        except errors.PyMongoError as err:
            print(f"An error occurred while creating a subject: {err}")
            return None
