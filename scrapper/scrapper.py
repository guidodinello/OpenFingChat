from scrapper.helpers.subjects import getSubjectsLinks, getSubject
from scrapper.helpers.lessons import getLesson, getLessonsTags

def scrapping():
    print("START SCRAPPING")
    subjectsLinks = getSubjectsLinks()

    for subjectLink in subjectsLinks:
        subjectName = subjectLink.split("/")[-2]
        print(f"### Start Scraping Subject {subjectName} ###")
        
        subject = getSubject(subjectLink)
        lessonsTags = getLessonsTags(subject["url"])

        for lessonTag in lessonsTags:
            lesson = getLesson(lessonTag, subject["_id"], subjectName)
            print(f"Lesson '{lesson["name"]}' successfully scrapped!")

        print(f"Subject '{subject["name"]}' successfully scrapped!")

    print("FINISH SCRAPPING")


