import unittest

from markdown_to_blocks import markdown_to_blocks

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


    def testno_blank_lines_returned(self):
        md = """
# Header 1



That was too much space.





## And so was that

**Yep!**



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Header 1",
                "That was too much space.",
                "## And so was that",
                "**Yep!**",
            ],
        )
