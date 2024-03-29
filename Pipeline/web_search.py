import re
import ssl

from pprint import pprint
from urllib.request import Request, urlopen
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from urllib.parse import quote_plus


def bing_search(query: str, pages_number=1) -> list:
    """
    Gets web results from Bing
    :param query: query to search
    :param pages_number: number of search pages to scrape
    :return: a list of links in ranked order
    """
    urls = []
    for page in range(pages_number):
        first = page * 10 + 1
        address = "https://www.bing.com/search?q=" + quote_plus(query) + '&first=' + str(first)
        data = get_html(address)
        soup = BeautifulSoup(data, 'lxml')
        links = soup.findAll('li', {'class': 'b_algo'})
        urls.extend([link.find('h2').find('a')['href'] for link in links])

    return urls


def duckduckgo_search(query: str, pages=1):
    urls = []
    start_index = 0
    for page in range(pages):
        address = "https://duckduckgo.com/html/?kl=en-us&q={}&s={}".format(quote_plus(query), start_index)
        data = get_html(address)
        soup = BeautifulSoup(data, 'lxml')
        links = soup.findAll('a', {'class': 'result__snippet'})
        urls.extend([link['href'] for link in links])
        start_index = len(urls)

    return urls


def get_html(url: str) -> str:
    """
    Downloads the html source code of a webpage
    :param url:
    :return: html source code
    """
    try:
        custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
        req = Request(url, headers={"User-Agent": custom_user_agent})
        gcontext = ssl.SSLContext()
        page = urlopen(req, timeout=5, context=gcontext)
        return str(page.read())
    except:
        return ''


class WebParser(HTMLParser):
    """
    A class for converting the tagged html to formats that can be used by a ML model
    """
    def __init__(self):
        super().__init__()
        self.block_tags = {
            'div', 'p'
        }
        self.inline_tags = {
            '', 'a', 'b', 'tr', 'main', 'span', 'time', 'td',
            'sup', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'em', 'strong', 'br'
        }
        self.allowed_tags = self.block_tags.union(self.inline_tags)
        self.opened_tags = []
        self.block_content = ''
        self.blocks = []

    def get_last_opened_tag(self):
        """
        Gets the last visited tag
        :return:
        """
        if len(self.opened_tags) > 0:
            return self.opened_tags[len(self.opened_tags) - 1]
        return ''

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        """
        Handles the start tag of an HTML node in the tree
        :param tag: the HTML tag
        :param attrs: the tag attributes
        :return:
        """
        self.opened_tags.append(tag)
        if tag in self.block_tags:
            self.block_content = self.block_content.strip()
            if len(self.block_content) > 0:
                if not self.block_content.endswith('.'):
                    self.block_content += '.'
                self.block_content = self.block_content.replace('\\n', ' ').replace('\\r', ' ')
                self.block_content = re.sub("\s\s+", " ", self.block_content)
                self.blocks.append(self.block_content)
            self.block_content = ''

    def handle_endtag(self, tag):
        """
        Handles the end tag of an HTML node in the tree
        :param tag: the HTML tag
        :return:
        """
        if len(self.opened_tags) > 0:
            self.opened_tags.pop()

    def handle_data(self, data):
        """
        Handles a text HTML node in the tree
        :param data: the text node
        :return:
        """
        last_opened_tag = self.get_last_opened_tag()
        if last_opened_tag in self.allowed_tags:
            data = data.replace('  ', ' ').strip()
            if data != '':
                self.block_content += data + ' '

    def get_text(self):
        return "\n\n".join(self.blocks)

      
