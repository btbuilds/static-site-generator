import unittest
from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "Just some text"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("Just some text", TextType.TEXT)])

    def test_bold_text(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ])

    def test_italic_text(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ])

    def test_code_text(self):
        text = "Here is `code` example"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" example", TextType.TEXT)
        ])

    def test_link_text(self):
        text = "Go to [Google](https://google.com)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Go to ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com")
        ])

    def test_image_text(self):
        text = "Here is ![alt](https://example.com/img.png)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Here is ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png")
        ])

    def test_mixed_formats(self):
        text = "This is **bold**, _italic_, `code`, a [link](https://example.com), and an image ![alt](https://example.com/img.png)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(", and an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png")
        ])

if __name__ == "__main__":
    unittest.main()
