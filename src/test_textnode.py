import unittest

from textnode import TextNode, TextType, text_node_to_html_node

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

class TestTextNodeConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_type_text(self):
        tn = TextNode("Just text", TextType.TEXT)
        node = text_node_to_html_node(tn)
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Just text")
        self.assertIsNone(node.props)

    def test_text_type_bold(self):
        tn = TextNode("Bold text", TextType.BOLD)
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "Bold text")
        self.assertIsNone(node.props)

    def test_text_type_italic(self):
        tn = TextNode("Italic text", TextType.ITALIC)
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "i")
        self.assertEqual(node.value, "Italic text")
        self.assertIsNone(node.props)

    def test_text_type_code(self):
        tn = TextNode("Code snippet", TextType.CODE)
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "code")
        self.assertEqual(node.value, "Code snippet")
        self.assertIsNone(node.props)

    def test_text_type_link(self):
        tn = TextNode("Click here", TextType.LINK, "https://example.com")
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click here")
        self.assertEqual(node.props, {"href": "https://example.com"})

    def test_text_type_image(self):
        tn = TextNode("An image", TextType.IMAGE, "https://img.com/pic.jpg")
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.props, {"src": "https://img.com/pic.jpg", "alt": "An image"})

if __name__ == "__main__":
    unittest.main()