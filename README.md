# webstoryparser

Parser for AMP web stories

## Usage

```
import requests
from webstory import Story

html = requests.get('https://www-bbc-co-uk.cdn.ampproject.org/c/s/www.bbc.co.uk/news/ampstories/moonmess/index.html').text
story = Story(html)

# Story metadata: title, publisher, publisher_logo_src, poster_portrait_src, poster_square_src, poster_landscape_src
story.title  # "What's left behind on the Moon?"
story.publisher  # "BBC"

# Pages
page = story.pages[0]
page.id  # "page-0"
page.html  # original HTML
page.get_clean_html()  # HTML filtered to valid AMP content only
```
