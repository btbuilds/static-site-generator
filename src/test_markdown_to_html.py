import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_levels(self):
        md = """# Heading 1

### Heading 3

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h3>Heading 3</h3><h6>Heading 6</h6></div>",
        )

    def test_blockquote(self):
        md = """> This is a blockquote
> with multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote\nwith multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """- Item one
- Item two
- Item three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_mixed_content(self):
        md = """# Title

Paragraph with **bold**, _italic_, and `code`.

- List item with a [link](https://example.com)
- Another with ![alt](image.png)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>Paragraph with <b>bold</b>, <i>italic</i>, and <code>code</code>.</p><ul><li>List item with a <a href=\"https://example.com\">link</a></li><li>Another with <img src=\"image.png\" alt=\"alt\"></li></ul></div>",
        )
