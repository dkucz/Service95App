from bs4 import BeautifulSoup
import requests

# testing
URL = 'https://www.service95.com/72-hours-in-marseille'

response = requests.get(URL)

print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')

def get_author_link() -> str:
    for link in soup.find_all('a'):
        href_res = link.get('href')
        if '/author' in href_res:
            return href_res

def get_author_name() -> str:
    author_href = get_author_link()
    author_arr = author_href.split('/')
    author_name_arr = author_arr[-1].split('-')
    author_name_arr[0] = author_name_arr[0].capitalize()
    author_name_arr[1] = author_name_arr[1].capitalize()
    return ' '.join(author_name_arr)

def get_article_title() -> str:
    return soup.title.text

def get_h1_text() -> str:
    return soup.h1.text

print('author_name: ' + get_author_name(), 'article_title: ' + get_article_title(), 'h1_text: ' + get_h1_text())

for image in soup.find_all(attrs={'as': 'image'}):
    print(image.get('href'))

for image in soup.find_all('img'):
    source = image.get('src')
    extensions = ['jpg', 'jpeg', 'png', 'gif']
    for extension in extensions:
        if extension in source:
            print(source)

article_wrapper = soup.find('div', class_='article-content-wrapper')
if article_wrapper:
    print(len(article_wrapper.find_all('p')))
    for p in article_wrapper.find_all('p'):
        print(p.text)


class Article:
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        # To be adjusted later
        self.author = None
        self.author_tag = None
        self.images = None
        self.paragraphs = None
        self.title = None
        self.h1_title = None
        # Init methods
        self._find_author_name()
        self._find_article_images()

    def _find_author_name(self) -> None:
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')
            if '/author' in href:
                a_tag_arr = href.split('/')
                author_arr = a_tag_arr[-1].split('-')
                author_arr[0] = author_arr[0].capitalize()
                author_arr[1] = author_arr[1].capitalize()
                author_name = ' '.join(author_arr)
                self.author_tag = a_tag_arr[-1]
                self.author = author_name
                break

    def _find_article_images(self) -> None:
        pass

    def get_author_name(self) -> str | None:
        return self.author

    def get_author_tag(self) -> str | None:
        return self.author_tag