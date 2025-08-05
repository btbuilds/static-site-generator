import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_equal_nodes(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_equal_text(self):
        node1 = TextNode("Some text", TextType.ITALIC)
        node2 = TextNode("Some other text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_equal_url_missing(self):
        node1 = TextNode("Link Text", TextType.LINK, "boot.dev")
        node2 = TextNode("Link Text", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_not_equal_url_none(self):
        node1 = TextNode("Link Text", TextType.LINK, "boot.dev")
        node2 = TextNode("Link Text", TextType.LINK, None)
        self.assertNotEqual(node1, node2)

    def test_equal_code_nodes(self):
        node1 = TextNode("Link Text", TextType.CODE, None)
        node2 = TextNode("Link Text", TextType.CODE, None)
        self.assertEqual(node1, node2)
    
    def test_not_equal_text_type(self):
        node1 = TextNode("Link Text", TextType.ITALIC, None)
        node2 = TextNode("Link Text", TextType.CODE, None)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()