import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("Badoop", TextType.NORMAL, "http://website.co")
        node2 = TextNode("Other thing", TextType.NORMAL, "http://website.co")
        self.assertNotEqual(node, node2)

    def test_not_eq_texttype(self):
        node = TextNode("Badoop", TextType.NORMAL, "http://website.co")
        node2 = TextNode("Badoop", TextType.LINK, "http://website.co")
        self.assertNotEqual(node, node2)

    def test_not_eq_site(self):
        node = TextNode("Badoop", TextType.NORMAL, "http://website.co")
        node2 = TextNode("Badoop", TextType.NORMAL, "http://poop.pee")
        self.assertNotEqual(node, node2)

    def test_wrong_enum(self):
        with self.assertRaises(AttributeError):
            TextNode("a", TextType.TURTLE)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
