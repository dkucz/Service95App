from bs4 import BeautifulSoup
import requests

# testing
URL = 'https://www.service95.com/72-hours-in-marseille'

class Article:
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        # Private attributes
        self._image_links = None
        self._article_wrapper = None
        # To be adjusted later
        self.author = None
        self.author_tag = None
        self.paragraphs = None
        self.title = None
        self.h1_title = None
        # Init methods
        self._find_author_name()
        self._find_article_images()
        self._find_paragraphs()
        self._find_titles()

    def _find_author_name(self) -> None:
        for a_tag in self.soup.find_all('a'):
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
        image_links = []
        supported_imgs = ['jpg', 'jpeg', 'png', 'gif']
        for image in self.soup.find_all('img'):
            source = image.get('src')
            for f_type in supported_imgs:
                if f_type in source:
                    image_links.append(source)
        self._image_links = image_links

    def _find_paragraphs(self) -> None:
        article_wrapper = self.soup.find('div', class_='article-content-wrapper')
        self._article_wrapper = article_wrapper
        paragraphs = []
        for p in article_wrapper.find_all('p'):
            paragraphs.append(p.text)
        self._article_wrapper = article_wrapper
        self.paragraphs = paragraphs

    def _find_titles(self) -> None:
        self.title = self.soup.title.text
        self.h1_title = self.soup.h1.text

    def get_author_name(self) -> str | None:
        return self.author

    def get_author_tag(self) -> str | None:
        return self.author_tag

    def get_image_links(self) -> list[str] | None:
        return self._image_links

    def get_paragraphs(self) -> list[str] | None:
        return self.paragraphs

    def get_article_wrapper(self):
        return self._article_wrapper

    def get_h1_title(self) -> str | None:
        return self.h1_title

    def get_title(self) -> str | None:
        return self.title