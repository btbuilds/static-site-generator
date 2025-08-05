import unittest

from htmlnode import HTMLNode


class TestHTMLNodePropsToHTML(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_single_prop(self):
        node = HTMLNode("a", "Click", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_multiple_props(self):
        node = HTMLNode("img", props={"src": "cat.jpg", "alt": "A cat", "width": "500"})
        result = node.props_to_html()
        expected_parts = ['src="cat.jpg"', 'alt="A cat"', 'width="500"']
        for part in expected_parts:
            self.assertIn(part, result)
        self.assertTrue(result.startswith(" "))
        self.assertEqual(result.count("="), 3)

    def test_empty_props_dict(self):
        node = HTMLNode("div", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_with_special_chars(self):
        node = HTMLNode("input", props={"type": "text", "placeholder": "Enter <value>"})
        result = node.props_to_html()
        self.assertIn('placeholder="Enter <value>"', result)
        self.assertIn('type="text"', result)
    
    def test_repr(self):
        node = HTMLNode("p", "Hello world", None, {"href": "https://www.example.com"})
        self.assertEqual(node.__repr__(), "HTMLNode(tag: p, value: Hello world, children: None, props: {'href': 'https://www.example.com'})")


if __name__ == "__main__":
    unittest.main()
