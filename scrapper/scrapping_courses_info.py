"""
Este script se encarga de extraer información sobre cursos y sus videos desde la página web de cursos de la Facultad de Ingeniería de la Universidad de la República (Uruguay).

El script realiza las siguientes funciones principales:
1. get_course_links(main_url): Obtiene todos los enlaces de los cursos desde la página principal de la lista de cursos.
2. get_course_name(course_url): Obtiene el nombre de un curso desde la página específica del curso.
3. get_video_names(course_url): Obtiene los nombres, números y URLs de los videos desde la página específica del curso.
4. scrape_courses(main_url): Función principal que coordina las funciones anteriores para extraer los enlaces de los cursos y la información de los videos, y los guarda en una estructura de datos.

El resultado se guarda en un archivo JSON llamado 'courses_data.json'.

URL de la lista principal de cursos: https://open.fing.edu.uy/courses/
"""

import requests
from bs4 import BeautifulSoup
import json

# Function to get all course links from the main course list
def get_course_links(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    course_links = []
    course_list = soup.find('div', class_='course-list')
    for a_tag in course_list.find_all('a', class_='name course', href=True):
        course_links.append(a_tag['href'])
    return course_links

# Function to get the course name from a course page
def get_course_name(course_url):
    response = requests.get(course_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    course_name = soup.find('div', class_='header__title').h1.text.strip()
    return course_name

# Function to get video names, numbers, and media URLs from a course page
def get_video_names(course_url):
    response = requests.get(course_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    videos = []
    course_name = course_url.split('/')[-2]
    for video_tag in soup.find_all('a', class_='class-list__item', href=True):
        video_number = video_tag.find('span', class_='class-list__item-number').text.strip()
        video_name = video_tag.find('div', class_='class-list__item-name').text.strip()
        video_url = video_tag['href']
        # Deriving media_url based on the video URL pattern
        media_url = f"https://open.fing.edu.uy/media/{course_name}/{course_name}_{video_number.zfill(2)}.mp4"
        videos.append({'number': video_number, 'name': video_name, 'url': video_url, 'media_url': media_url})
    return videos

# Main function to scrape course links and their video names
def scrape_courses(main_url):
    courses_info = []
    course_links = get_course_links(main_url)
    for course_link in course_links:
        print(f"Scraping course: {course_link}")
        course_name = get_course_name(course_link)
        video_names = get_video_names(course_link)
        courses_info.append({'name': course_name, 'url': course_link, 'videos': video_names})
    return courses_info

# URL of the main course list
main_url = 'https://open.fing.edu.uy/courses/'

# Scrape courses and get the result
courses_info = scrape_courses(main_url)

# Save the result to a JSON file
with open('courses_data.json', 'w', encoding='utf-8') as f:
    json.dump(courses_info, f, ensure_ascii=False, indent=4)

print("Data has been saved to courses_data.json")
