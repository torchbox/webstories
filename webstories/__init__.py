import copy
from bs4 import BeautifulSoup

from .cleaner import StoryPageCleaner


class Story:
    class InvalidStoryException(ValueError):
        pass

    def __init__(self, html):
        self._dom = BeautifulSoup(html, 'html.parser')
        self._story_node = self._dom.find('amp-story')

        if not self._story_node:
            raise Story.InvalidStoryException("The passed HTML is not a valid web story")

        self.title = self._story_node.get('title')
        self.publisher = self._story_node.get('publisher')
        self.publisher_logo_src = self._story_node.get('publisher-logo-src')
        self.poster_portrait_src = self._story_node.get('poster-portrait-src')
        self.poster_square_src = self._story_node.get('poster-square-src')
        self.poster_landscape_src = self._story_node.get('poster-landscape-src')

        self.pages = [
            StoryPage(node)
            for node in self._story_node.find_all('amp-story-page', recursive=False)
        ]

        custom_css_node = self._dom.find('style', attrs={'amp-custom': True})
        self.custom_css = custom_css_node and custom_css_node.text

    def __str__(self):
        return "<Story: %s>" % self.title

    def __repr__(self):
        return str(self)


class StoryPage:
    def __init__(self, node):
        self._node = node

        self.id = self._node.get('id')

    @property
    def html(self):
        return str(self._node)

    def get_clean_html(self):
        # reject <script> tags without an allowed type attribute, as per
        # https://amp.dev/documentation/guides-and-tutorials/learn/spec/amphtml/?format=websites#html-tags
        # (we can't do this within a bleach Cleaner instance)
        node = copy.copy(self._node)
        return StoryPage._clean_html_from_node(node)

    @staticmethod
    def clean_html_fragment(html):
        """
        Given an HTML fragment with <amp-story-page> as its root element, return a version with
        non-AMP-valid tags removed
        """
        node = BeautifulSoup(html, 'html.parser')
        return StoryPage._clean_html_from_node(node)

    @staticmethod
    def _clean_html_from_node(node):
        """
        Return the AMP-cleaned version of a BeautifulSoup DOM node object, as an HTML string.
        May modify the node object.
        """
        # reject <script> tags without an allowed type attribute, as per
        # https://amp.dev/documentation/guides-and-tutorials/learn/spec/amphtml/?format=websites#html-tags
        # (we can't do this within a bleach Cleaner instance)
        for script in node.find_all('script'):
            if script.get('type') not in ('application/ld+json', 'application/json', 'text/plain'):
                script.extract()
        html_without_scripts = str(node)
        return StoryPageCleaner().clean(html_without_scripts)

    def __str__(self):
        return "<StoryPage: %s>" % self.id

    def __repr__(self):
        return str(self)
