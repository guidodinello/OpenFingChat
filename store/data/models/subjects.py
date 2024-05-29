from bson import ObjectId
from pymongo import errors
from store.data.connection import getDatabase
from store.data.models.lessons import LessonModel

class SubjectModel:

    def __init__(self):
        try:
            db = getDatabase()
            self.collection = db['subjects']
            self.collection.create_index([('url', 1)], unique=True)
        except ConnectionError as err:
            print(err)
            raise RuntimeError(f"Initialization failed: {err}")
        
    def get(self, subjectId, withLessons = False):
        try:
            subject = self.collection.find_one({"_id": ObjectId(subjectId)})
            if subject and withLessons:
                lessons = LessonModel()
                subject["lessons"] = lessons.getAll({"subjectId": ObjectId(subjectId)})

            return subject
        except errors.PyMongoError as err:
            print(f"An error occurred while retrieving the subject: {err}")
            return None
    
    def getBy(self, filters = {}):
        try:
            subject = self.collection.find_one(filters)
            return subject
        except errors.PyMongoError as err:
            print(f"An error occurred while retrieving the subject: {err}")
            return None

    def getAll(self, filters = {}):       
        try:
            subjects = self.collection.find(filters)
            return list(subjects)
        except errors.PyMongoError as err:
            print(f"An error occurred while retrieving all subjects: {err}")
            return []
        
    def create(self, name, url):
        try:
            result = self.collection.insert_one({ "name": name, "url": url })

            return result.inserted_id
        except errors.DuplicateKeyError:
            return None
        except errors.PyMongoError as err:
            print(f"An error occurred while creating a subject: {err}")
            return None
