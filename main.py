import logging
import sys

import constants
from loader import loader
from scrapper import scrapper
from store.mongo.models.lessons import LessonModel
from store.mongo.models.subjects import SubjectModel
from transcriptor import transcriptor

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.info("Usage: python main.py <script> [<args>]")
        sys.exit(1)

    _, script, *script_args = sys.argv

    logging.info(
        "Running script: %s with configuration file %s", script, constants.CONFIG_FILE
    )

    lesson = LessonModel()
    subject = SubjectModel()

    if script == "scrapper":
        scrapper.scrapping(lesson, subject)
    elif script == "loader":
        loader.main(script_args)
    elif script == "transcriptor":
        subjects_names = [
            "Mecánica Newtoniana",
            "Electrónica Fundamental",
            "Señales y Sistemas",
        ]
        transcriptor.transcript(subjects_names, max_lessons=10)
    else:
        logging.info("Unknown script: %s", script)
        sys.exit(1)
