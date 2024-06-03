import logging
import sys

from loader import loader
from scrapper.scrapper import scrapping

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.info("Usage: python main.py <script> [<args>]")
        sys.exit(1)

    _, script, *script_args = sys.argv

    if script == "scrapping":
        scrapping()
    elif script == "loader":
        loader.main(script_args)
    else:
        logging.info(f"Unknown script: {script}")
        sys.exit(1)
