import unittest
from block_markdown import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_paragraph(self):
        md = "Just a single paragraph with no breaks."
        self.assertEqual(
            markdown_to_blocks(md),
            ["Just a single paragraph with no breaks."]
        )

    def test_leading_and_trailing_whitespace(self):
        md = "   First paragraph with spaces    \n\n   Second paragraph    "
        self.assertEqual(
            markdown_to_blocks(md),
            ["First paragraph with spaces", 
             "Second paragraph"]
        )

    def test_multiple_blank_lines(self):
        md = "First paragraph\n\n\n\nSecond paragraph"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First paragraph", 
             "Second paragraph"]
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace_string(self):
        self.assertEqual(markdown_to_blocks("   \n  \n"), [])
