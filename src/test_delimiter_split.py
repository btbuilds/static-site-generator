import unittest
from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter  # Replace with your actual module name

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiters(self):
        node = TextNode("No formatting here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_single_delimiter_pair(self):
        node = TextNode("This has `code` inside", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" inside", TextType.TEXT)
        ])

    def test_multiple_delimiter_pairs(self):
        node = TextNode("Mix of `code` and `more code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("Mix of ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" here", TextType.TEXT)
        ])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has `unmatched delimiters", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_delimiter_at_start(self):
        node = TextNode("`start` then text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("start", TextType.CODE),
            TextNode(" then text", TextType.TEXT)
        ])

    def test_delimiter_at_end(self):
        node = TextNode("text then `end`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("text then ", TextType.TEXT),
            TextNode("end", TextType.CODE)
        ])

    def test_non_text_nodes_unchanged(self):
        node = TextNode("Already code", TextType.CODE)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_multiple_same_type(self):
        node = TextNode("Some _italic_ and some more _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0], TextNode("Some ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" and some more ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("italic", TextType.ITALIC))

    def test_invalid_syntax_raises(self):
        node = TextNode("This is **bold", TextType.TEXT)  # no closing **
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
