import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_image, split_nodes_link

class TestSplitImages(unittest.TestCase):
    def test_single_image_only(self):
        node = TextNode(
            "![only](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("only", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode(
            "![start](https://example.com/img.png) and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" and some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode(
            "Some text then ![end](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some text then ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("Just some plain text here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Just some plain text here.", TextType.TEXT)],
            new_nodes,
        )

    def test_non_text_nodes_unchanged(self):
        node = TextNode("Already image", TextType.IMAGE, "https://example.com/img.png")
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Already image", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

class TestSplitLinks(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "This has a [link](https://example.com) inside.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" inside.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_links(self):
        node = TextNode(
            "Visit [Google](https://google.com) or [GitHub](https://github.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" or ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("No links here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("No links here.", TextType.TEXT)],
            new_nodes,
        )

    def test_non_text_nodes_unchanged(self):
        node = TextNode("Already a link", TextType.LINK, "https://something.com")
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("Already a link", TextType.LINK, "https://something.com")],
            new_nodes,
        )