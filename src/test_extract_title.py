import unittest
from block_markdown import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_title_with_extra_spaces(self):
        md = "#    Spaced Out   "
        self.assertEqual(extract_title(md), "Spaced Out")

    def test_title_not_first_line(self):
        md = "Some intro\n\n# My Title\n\nMore stuff"
        self.assertEqual(extract_title(md), "My Title")

    def test_multiple_titles_returns_first(self):
        md = "# First Title\n\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")

    def test_no_title_raises(self):
        md = "Just some text\n\nNot a title"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_title_with_punctuation(self):
        md = "# Hello, World!"
        self.assertEqual(extract_title(md), "Hello, World!")

    def test_h2_does_not_count(self):
        md = "## Subheading"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_title_with_hash_but_no_space(self):
        md = "#NoSpaceTitle"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_only_hash_and_space(self):
        md = "# "
        self.assertEqual(extract_title(md), "")

if __name__ == "__main__":
    unittest.main()
