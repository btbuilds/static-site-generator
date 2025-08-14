import unittest
from block_markdown import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        md = "# Heading 1"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    def test_code_block(self):
        md = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_quote_block(self):
        md = "> First line\n> Second line"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_unordered_list(self):
        md = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED)

    def test_ordered_list_valid(self):
        md = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED)

    def test_ordered_list_invalid_numbering(self):
        md = "1. First\n3. Third\n4. Fourth"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = "This is just some text, not a list or heading."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
