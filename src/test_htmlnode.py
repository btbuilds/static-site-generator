import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Click me</a>')

    def test_leaf_to_html_plain_text(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "This is a div")
        self.assertEqual(node.to_html(), "<div>This is a div</div>")

    def test_leaf_to_html_br_invalid(self):
        with self.assertRaises(ValueError):
            node = LeafNode("br", "")
            node.to_html()

    def test_leaf_to_html_none_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_leaf_to_html_text_only(self):
        node = LeafNode(None, "Just text, no tag")
        self.assertEqual(node.to_html(), "Just text, no tag")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "First")
        child2 = LeafNode("p", "Second")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><p>First</p><p>Second</p></div>")

    def test_to_html_with_props(self):
        child = LeafNode("span", "Text")
        parent_node = ParentNode("div", [child], props={"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>Text</span></div>',
        )

    def test_raises_error_without_tag(self):
        with self.assertRaises(ValueError):
            # Intentionally removing tag (None instead of str)
            node = ParentNode(None, [LeafNode("p", "Text")])  # type: ignore
            node.to_html()

    def test_raises_error_without_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", [])
            node.to_html()

if __name__ == "__main__":
    unittest.main()
