# webstories

Python parser for AMP web stories

## Usage

```python
import requests
from webstories import Story

html = requests.get('https://www.bbc.co.uk/news/ampstories/moonmess/index.html').text
story = Story(html)

# Story metadata: title, publisher, publisher_logo_src, poster_portrait_src, poster_square_src, poster_landscape_src
story.title  # "What's left behind on the Moon?"
story.publisher  # "BBC"

story.custom_css  # text content of the <style amp-custom> element, or None if none exists

# Pages
page = story.pages[0]
page.id  # "page-0"
page.html  # original HTML
page.get_clean_html()  # HTML filtered to valid AMP content only

# Standalone HTML cleaning
from webstories import StoryPage

StoryPage.clean_html_fragment(
    """<amp-story-page id="scary-ghost" onclick="alert('boo')"></amp-story-page>"""
)
# returns: '<amp-story-page id="scary-ghost"></amp-story-page>'
```
