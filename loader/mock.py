# mock
MONGO_CLIENT = {
    "database": {
        "classes": [
            {"_id": 1, "name": "plogica01.json", "url": "plogica/01.mp4"},
            {"_id": 2, "name": "plogica02.json", "url": "plogica/02.mp4"},
        ],
    }
}


class CustomList(list):
    def find(self, query, projection=None):
        if query == {}:
            res = [doc["_id"] for doc in self]
            print(res)
            return res
        else:
            pass


# Define a custom find method for the "classes" list
MONGO_CLIENT["database"]["classes"] = CustomList(MONGO_CLIENT["database"]["classes"])
