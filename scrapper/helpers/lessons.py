import os
from dotenv import load_dotenv
from scrapper.helpers.utils import getPageContent
from store.data.models.lessons import LessonModel

load_dotenv(override=True)
OPENFING_URL = os.environ['OPENFING_URL']

def getLessonsTags(subjectURL):
    content = getPageContent(subjectURL)
    
    return content.find_all("a", class_="class-list__item", href=True)

def getLesson(tag, subjectId, subjectName):
    url = getLessonURL(tag)
    name = getLessonName(tag)
    video = getVideoLink(tag, subjectName)

    lessons = LessonModel()
    
    id = lessons.create(subjectId, name, url, video)
    if id:
        lesson = lessons.get(id)   
    else:
        lesson = lessons.getBy({"url":url})

    return lesson

def getLessonName(tag):
    return tag.find("div", class_="class-list__item-name").text.strip()

def getVideoLink(tag, subjectName):
    number = tag.find("span", class_="class-list__item-number").text.strip()

    return f"{OPENFING_URL}/media/{subjectName}/{subjectName}_{number.zfill(2)}.mp4"

def getLessonURL(tag):
    return tag["href"]
