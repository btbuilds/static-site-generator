import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "![first](http://example.com/1.png) some text ![second](http://example.com/2.png)"
        )
        self.assertListEqual(
            [
                ("first", "http://example.com/1.png"),
                ("second", "http://example.com/2.png"),
            ],
            matches,
        )

    def test_no_images(self):
        matches = extract_markdown_images("This text has no images at all.")
        self.assertListEqual([], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        matches = extract_markdown_links(
            "Here is a [link](https://example.com) in text."
        )
        self.assertListEqual(
            [("link", "https://example.com")], matches
        )

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "[first](http://example.com/1) and [second](http://example.com/2)"
        )
        self.assertListEqual(
            [
                ("first", "http://example.com/1"),
                ("second", "http://example.com/2"),
            ],
            matches,
        )

    def test_no_links(self):
        matches = extract_markdown_links("No markdown links here.")
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()
