# from store.data.models.subjects import SubjectModel
# from store.data.models.lessons import LessonModel

# model = SubjectModel()

# id = model.create("AGPI", "fklgdflgnlkdngkdfnglkdfngkdlfnxg")
# print(f"ID {id}\n")

# s = model.get(id)
# print(f"Retrieved subject: {s}\n")

# all = model.getAll()
# print(f"All subjects: {all}\n")


# lessons = LessonModel()
# id1 = lessons.create(id, "Clase 1","url1", "videourl1")
# id2 = lessons.create(id, "Clase 2","url2", "videourl2")

# allS = lessons.getAll()
# print(f"All lessons: {allS}\n")

# s1 = lessons.get(id1)
# print(f"Retrieved Lesson: {s1}\n")

# lessons.update(id1, {"transcribed": True})

# sTranscribed = lessons.getBy({"transcribed": False})
# print(f"Retrieved Lesson Not Transcribed: {sTranscribed}\n")


# sWithLessons = model.get(id, True)
# print(f"Retrieved subject with lessons: {sWithLessons}\n")

import sys
from scrapper.scrapper import scrapping

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <arg1>")
        sys.exit(1)

    script = sys.argv[1]

    if script == "scrapping":   
        scrapping()