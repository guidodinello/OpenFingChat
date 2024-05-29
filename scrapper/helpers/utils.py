from bs4 import BeautifulSoup
import requests


def getPageContent(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    return soup