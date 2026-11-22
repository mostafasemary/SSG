import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_single_line_title(self):
        title = extract_title("# Hello")
        self.assertEqual(title, "Hello")

    def test_title_with_extra_whitespace(self):
        title = extract_title("#   Hello   ")
        self.assertEqual(title, "Hello")

    def test_multiline_with_subheadings(self):
        md = """
## Subheading before

Some intro paragraph.

# The Real Title

## Subheading after
"""
        title = extract_title(md)
        self.assertEqual(title, "The Real Title")

    def test_no_h1_raises_exception(self):
        md = """
## Only an h2 heading

Just a normal paragraph with no h1.
"""
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
