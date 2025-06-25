from enum import Enum
import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("Badoop", TextType.TEXT, "http://website.co")
        node2 = TextNode("Other thing", TextType.TEXT, "http://website.co")
        self.assertNotEqual(node, node2)

    def test_not_eq_texttype(self):
        node = TextNode("Badoop", TextType.TEXT, "http://website.co")
        node2 = TextNode("Badoop", TextType.LINK, "http://website.co")
        self.assertNotEqual(node, node2)

    def test_not_eq_site(self):
        node = TextNode("Badoop", TextType.TEXT, "http://website.co")
        node2 = TextNode("Badoop", TextType.TEXT, "http://poop.pee")
        self.assertNotEqual(node, node2)

    def test_wrong_enum(self):
        with self.assertRaises(AttributeError):
            TextNode("a", TextType.TURTLE)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_invalid_enum(self):
        # What if someone adds an enum that isn't in the case match of
        # text_node_to_html()? It's a valid enum, but not a valid value.
        TextTypeTest = Enum("TextTypeTest", ["ANIMAL"])

        node = TextNode("This is a weird node!", TextTypeTest.ANIMAL)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )


if __name__ == "__main__":
    unittest.main()
