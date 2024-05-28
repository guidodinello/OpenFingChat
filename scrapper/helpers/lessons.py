import os
from dotenv import load_dotenv
from urllib.parse import urljoin
from scrapper.helpers.utils import getPageContent
from store.data.models.lessons import LessonModel

load_dotenv(override=True)
OPENFING_URL = os.environ['OPENFING_URL']

def getLessonsLinks(subjectURL):
    content = getPageContent(subjectURL)

    links = []
    lessons = content.find_all("a", class_="class-list__item", href=True)

    for link in lessons:
        links.append(link["href"])
    
    return links

def getLesson(url, subjectId):
    content = getPageContent(url)

    name = getLessonName(content)
    video = getVideoLink(content)

    lessons = LessonModel()
    
    id = lessons.create(subjectId, name, url, video)
    if id:
        lesson = lessons.get(id)   
    else:
        lesson = lessons.getBy({"url":url})

    return lesson

def getLessonName(content):
    return content.find("div", class_="title__container").h2.text.strip()

def getVideoLink(content):
    button = content.find("a", attrs={'download': True})

    return urljoin(OPENFING_URL, button['href'])
