from store.data.models.subjects import SubjectModel
# model = SubjectModel()

id = SubjectModel.create("AGPI", "fklgdflgnlkdngkdfnglkdfngkdlfnxg")
print("ID {id}")

s = SubjectModel.get(id)
print(f"Retrieved subject: {s}")

all = SubjectModel.getAll()
print(f"All subjects: {all}")