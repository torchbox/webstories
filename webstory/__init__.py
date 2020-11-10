from bs4 import BeautifulSoup


class Story:
    def __init__(self, html):
        self._dom = BeautifulSoup(html, 'html.parser')
        self._story_node = self._dom.find('amp-story')

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

    def __str__(self):
        return "<StoryPage: %s>" % self.id

    def __repr__(self):
        return str(self)
