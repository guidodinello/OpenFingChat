import os
from dotenv import load_dotenv
from scrapper.helpers.utils import getPageContent
from store.data.models.subjects import SubjectModel

load_dotenv(override=True)
OPENFING_URL = os.environ['OPENFING_URL']

def getSubjectsLinks():
    url = f"{OPENFING_URL}/courses/"
    content = getPageContent(url)

    links = []
    subjects = content.find("div", class_="course-list")

    for link in subjects.find_all("a", class_="name course", href=True):
        links.append(link["href"])

    return links

def getSubject(url):
    content = getPageContent(url)
    name = getSubjectName(content)

    subjects = SubjectModel()

    id = subjects.create(name, url)
    if id:
        subject = subjects.get(id)
    else:
        subject = subjects.getBy({"url":url})

    return subject

def getSubjectName(content):
    return content.find("div", class_="header__title").h1.text.strip()

