import logging

import bs4
import requests  # TODO: replace with httpx, also use bulk writes to the mongo db

import constants


def page_content(url):
    response = requests.get(url, timeout=10)
    return bs4.BeautifulSoup(response.content, "html.parser")


def subject_lessons(subject_link):
    return page_content(subject_link).find_all(
        "a", class_="class-list__item", href=True
    )


def subjects(url):
    course_list = page_content(f"{url}/courses/").find("div", class_="course-list")

    for subject in course_list.find_all(
        "a", class_="name course", href=True
    ):  # subjects could be processed in parallel
        name = subject.find("span", class_="course-title").text
        link = subject["href"]
        yield name, link


def scrapping(db_lesson, db_subject):
    logging.info("START SCRAPPING")

    for s_name, s_link in subjects(constants.OPENFING_URL):
        s_id = db_subject.create(s_name, s_link)
        logging.info("### Scraping Subject  %s  ###", s_name)

        for lesson in subject_lessons(s_link):  # lessons could be processed in parallel
            link = lesson["href"]
            name = lesson.find("div", class_="class-list__item-name").text.strip()

            video = video_url(link)
            lesson = db_lesson.create(s_id, name, link, video)
            logging.info("Lesson ' %s ' successfully scrapped!", name)

        logging.info("Subject ' %s ' successfully scrapped!", s_name)

    logging.info("FINISH SCRAPPING")


def video_url(lesson_link: str):
    download_button = page_content(lesson_link).find(
        "div", class_="video__interactions"
    )
    return f"{constants.OPENFING_URL}{download_button.find('a', href=True)['href']}"


def update_lessons_url(db_lesson):
    for lesson in db_lesson.get_all():
        video = video_url(lesson["link"])
        lesson = db_lesson.update(lesson["_id"], {"video": video})


if __name__ == "__main__":
    ...
