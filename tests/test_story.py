import unittest
from bs4 import BeautifulSoup

from webstory import Story


class TestStory(unittest.TestCase):
    def setUp(self):
        self.example_html = """
<!doctype html>
<html ⚡>
  <head>
    <meta charset="utf-8">
    <title>Joy of Pets</title>
    <link rel="canonical" href="pets.html">
    <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
    <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
    <script async src="https://cdn.ampproject.org/v0.js"></script>
    <script async custom-element="amp-video"
        src="https://cdn.ampproject.org/v0/amp-video-0.1.js"></script>
    <script async custom-element="amp-story"
        src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>
    <style amp-custom>
    </style>
  </head>
  <body>
    <!-- Cover page -->
    <amp-story standalone
        title="Joy of Pets"
        publisher="AMP tutorials"
        publisher-logo-src="assets/AMP-Brand-White-Icon.svg"
        poster-portrait-src="assets/cover.jpg">
      <amp-story-page id="cover">
        <amp-story-grid-layer template="fill">
          <amp-img src="assets/cover.jpg"
              width="720" height="1280"
              layout="responsive">
          </amp-img>
        </amp-story-grid-layer>
        <amp-story-grid-layer template="vertical">
          <h1>The Joy of Pets</h1>
          <p>By AMP Tutorials</p>
        </amp-story-grid-layer>
      </amp-story-page>

      <!-- Page 1 -->
      <amp-story-page id="page1">
        <amp-story-grid-layer template="vertical">
          <h1>Cats</h1>
          <amp-img src="assets/cat.jpg"
              width="720" height="1280"
              layout="responsive">
          </amp-img>
          <q>Dogs come when they're called. Cats take a message and get back to you. --Mary Bly</q>
        </amp-story-grid-layer>
      </amp-story-page>
    </amp-story>
  </body>
</html>
        """

        self.example_bad_html = """
<!doctype html>
<html ⚡>
  <head>
    <meta charset="utf-8">
    <title>Joy of Pets</title>
    <link rel="canonical" href="pets.html">
    <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
    <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
    <script async src="https://cdn.ampproject.org/v0.js"></script>
    <script async custom-element="amp-video"
        src="https://cdn.ampproject.org/v0/amp-video-0.1.js"></script>
    <script async custom-element="amp-story"
        src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>
    <style amp-custom>
    </style>
  </head>
  <body>
    <!-- Cover page -->
    <amp-story standalone
        title="Joy of Pets"
        publisher="AMP tutorials"
        publisher-logo-src="assets/AMP-Brand-White-Icon.svg"
        poster-portrait-src="assets/cover.jpg">
      <amp-story-page id="cover">
        <amp-story-grid-layer template="fill" data-coffee="yes" sugar="no">
          <script>alert('evil javascript');</script>
          <script type="application/json">{"text": "JSON is OK"}</script>
          <amp-img src="assets/cover.jpg"
              width="720" height="1280"
              layout="responsive">
          </amp-img>
        </amp-story-grid-layer>
        <amp-story-grid-layer template="vertical">
          <h1>The Joy of Pets</h1>
          <p>By AMP Tutorials</p>
          <form>
            <p>look at me, I'm in a form</p>
          </form>
        </amp-story-grid-layer>
      </amp-story-page>
    </amp-story>
  </body>
</html>
        """

    def assertHTMLEqual(self, str1, str2):
        soup1 = BeautifulSoup(str1.strip(), 'html.parser')
        soup2 = BeautifulSoup(str2.strip(), 'html.parser')
        self.assertEqual(soup1, soup2)

    def test_properties(self):
        story = Story(self.example_html)
        self.assertEqual(story.title, "Joy of Pets")
        self.assertEqual(story.publisher, "AMP tutorials")

        self.assertEqual(story.pages[0].id, "cover")

    def test_clean_html(self):
        story = Story(self.example_html)
        expected_clean_html = """
            <amp-story-page id="page1">
                <amp-story-grid-layer template="vertical">
                    <h1>Cats</h1>
                    <amp-img height="1280" layout="responsive" src="assets/cat.jpg" width="720">
                    </amp-img>
                    <q>Dogs come when they're called. Cats take a message and get back to you. --Mary Bly</q>
                </amp-story-grid-layer>
            </amp-story-page>
        """
        self.assertHTMLEqual(story.pages[1].get_clean_html(), expected_clean_html)

        story = Story(self.example_bad_html)
        expected_clean_html = """
            <amp-story-page id="cover">
                <amp-story-grid-layer template="fill" data-coffee="yes">
                    <script type="application/json">{"text": "JSON is OK"}</script>
                    <amp-img src="assets/cover.jpg" width="720" height="1280" layout="responsive">
                    </amp-img>
                </amp-story-grid-layer>
                <amp-story-grid-layer template="vertical">
                    <h1>The Joy of Pets</h1>
                    <p>By AMP Tutorials</p>
                    <p>look at me, I'm in a form</p>
                </amp-story-grid-layer>
            </amp-story-page>
        """
        self.assertHTMLEqual(story.pages[0].get_clean_html(), expected_clean_html)
