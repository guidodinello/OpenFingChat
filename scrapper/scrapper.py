from scrapper.helpers.subjects import getSubjectsLinks, getSubject
from scrapper.helpers.lessons import getLessonsLinks, getLesson

def scrapping():
    subjectsLinks = getSubjectsLinks()

    for subjectLink in subjectsLinks:
        print(f"Start Scraping Subject {subjectLink}")
        
        subject = getSubject(subjectLink)
        lessonsLinks = getLessonsLinks(subject["url"])

        for lessonLink in lessonsLinks:
            print(f"Start Scraping Lesson {lessonLink}")
            lesson = getLesson(lessonLink, subject["_id"])
            print(f"End Scrapping Lesson '{lesson["name"]}'")

        print(f"End Scraping Subject '{subject["name"]}'")


