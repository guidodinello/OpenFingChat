from bson import ObjectId
from pymongo import errors

from store.data.connection import getDatabase
from store.data.models.subjects import SubjectModel


class LessonModel:
    def __init__(self):
        try:
            db = getDatabase()
            self.collection = db["lessons"]
            self.collection.create_index([("url", 1)], unique=True)
        except ConnectionError as err:
            print(err)
            raise RuntimeError(f"Initialization failed: {err}")

    def get(self, lessonId, withSubject = False):
        try:
            lesson = self.collection.find_one({"_id": ObjectId(lessonId)})
            if lesson and withSubject:
                lessons = SubjectModel()
                lesson["subject"] = lessons.get(lesson["subjectId"])
            return lesson
        except errors.PyMongoError as err:
            print(f"An error occurred while retrieving the lesson: {err}")
            return None

    def getBy(self, filters={}):
        try:
            lesson = self.collection.find_one(filters)
            return lesson
        except errors.PyMongoError as err:
            print(f"An error occurred while retrieving the lesson: {err}")
            return None

    def getAll(self, **kwargs):
        try:
            lessons = self.collection.find(kwargs)
            return list(lessons)
        except errors.PyMongoError as err:
            print(f"An error occurred while retrieving all lessons: {err}")
            return []

    def create(self, subjectId, name, url, video):
        try:
            result = self.collection.insert_one(
                {
                    "name": name,
                    "url": url,
                    "video": video,
                    "transcribed": False,
                    "subjectId": ObjectId(subjectId),
                }
            )

            return result.inserted_id
        except errors.DuplicateKeyError:
            return None
        except errors.PyMongoError as err:
            print(f"An error occurred while creating a subject: {err}")
            return None

    def update(self, lessonId, data):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(lessonId)}, {"$set": data}
            )
            return result.modified_count
        except errors.PyMongoError as err:
            print(f"An error occurred while updating the user: {err}")
            return None
