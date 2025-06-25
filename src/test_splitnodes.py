import unittest

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_straightforward_cases(self):
        n1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        res1 = split_nodes_delimiter([n1], "`", TextType.CODE)
        expt1 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        n2 = TextNode("A **bolded** word.", TextType.TEXT)
        res2 = split_nodes_delimiter([n2], "**", TextType.BOLD)
        expt2 = [
            TextNode("A ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
        ]

        n3 = TextNode("An _italicised_ word.", TextType.TEXT)
        res3 = split_nodes_delimiter([n3], "_", TextType.ITALIC)
        expt3 = [
            TextNode("An ", TextType.TEXT),
            TextNode("italicised", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
        ]

        self.assertEqual(res1, expt1)
        self.assertEqual(res2, expt2)
        self.assertEqual(res3, expt3)

    def test_empty_input(self):
        n = TextNode("", TextType.TEXT)
        res = split_nodes_delimiter([n], "_", TextType.ITALIC)
        expt = []

        self.assertEqual(res, expt)

    def test_nested(self):
        n = TextNode("Well **that's just _terrible_**!", TextType.TEXT)

        res1 = split_nodes_delimiter([n], "_", TextType.ITALIC)
        expt1 = [
            TextNode("Well **that's just ", TextType.TEXT),
            TextNode("terrible", TextType.ITALIC),
            TextNode("**!", TextType.TEXT),
        ]

        res2 = split_nodes_delimiter([n], "**", TextType.BOLD)
        expt2 = [
            TextNode("Well ", TextType.TEXT),
            TextNode("that's just _terrible_", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]

        self.assertEqual(res1, expt1)
        self.assertEqual(res2, expt2)

    def test_non_text(self):
        n = TextNode("Well **that's just _terrible_**!", TextType.CODE)

        res = split_nodes_delimiter([n], "**", TextType.BOLD)
        expt = [TextNode("Well **that's just _terrible_**!", TextType.CODE)]

        self.assertEqual(res, expt)

    def test_wrong_delimiter_for_text(self):
        n = TextNode("Well **that's just _terrible_**!", TextType.TEXT)

        res = split_nodes_delimiter([n], "`", TextType.CODE)
        expt = [TextNode("Well **that's just _terrible_**!", TextType.TEXT)]

        self.assertEqual(res, expt)

    def test_unmatched_delim_throws_error(self):
        n = TextNode("Somethin' just ain't **right here", TextType.TEXT)

        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([n], "**", TextType.BOLD)

        excp = cm.exception
        self.assertEqual(
            excp.__str__(),
            "Odd number of delimiter (**) found. Markdown delimiters should come in pairs, e.g. `inline code` or **bold text**",
        )
