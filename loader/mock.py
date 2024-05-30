# mock
MONGO_CLIENT = {
    "database": {
        "classes": [
            {
                "_id": "ObjectId('665689bf97cf1d12f0260f43')",
                "name": "Enrutamiento Interno: Introducción",
                "url": "https://open.fing.edu.uy/courses/redes2/4/",
                "video": "https://open.fing.edu.uy/media/redes2/redes2_04.mp4",
                "transcribed": False,
                "subjectId": "ObjectId('665689ba97cf1d12f0260f3b')",
            },
            {
                "_id": "ObjectId('665689c097cf1d12f0260f45')",
                "name": "OSPF - Clase 1",
                "url": "https://open.fing.edu.uy/courses/redes2/5/",
                "video": "https://open.fing.edu.uy/media/redes2/redes2_05.mp4",
                "transcribed": False,
                "subjectId": "ObjectId('665689ba97cf1d12f0260f3b')",
            },
        ],
    }
}


class CustomList(list):
    def find(self, filters=None, projection=None):
        if filters == {"transcribed": True} and projection == {"_id": 1}:
            # eliminar ObjectId()
            format_id = lambda x: x.split("'")[1]
            res = [format_id(doc["_id"]) for doc in self]
            return res
        else:
            pass


# Define a custom find method for the "classes" list
MONGO_CLIENT["database"]["classes"] = CustomList(MONGO_CLIENT["database"]["classes"])

# from mock import MONGO_CLIENT

# lessons_id = MONGO_CLIENT["database"]["classes"].find(
#     {"transcribed": True},
#     projection={"_id": 1},
# )
