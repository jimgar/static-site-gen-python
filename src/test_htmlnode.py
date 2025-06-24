import unittest

from htmlnode import LeafNode, HTMLNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"cats": "beautiful", "dogs": "ok"})
        expected = ' cats="beautiful" dogs="ok"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        tag = "p"
        value = "Nolly is a cat"
        props = {"cats": "beautiful", "dogs": "ok"}

        node = HTMLNode(tag, value, props=props)
        expected = f"HTMLNode({tag}, {value}, {None}, {props})"
        self.assertEqual(node.__repr__(), expected)

    def test_props_to_html_none(self):
        node = HTMLNode()
        expected = ""
        self.assertEqual(node.props_to_html(), expected)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "I'm a link", {"href": "http://open-ai-are-cunts.com"})
        self.assertEqual(
            node.to_html(), '<a href="http://open-ai-are-cunts.com">I\'m a link</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node1 = LeafNode("", "Hello, world!")
        self.assertEqual(node1.to_html(), "Hello, world!")

        node2 = LeafNode(None, "Hello, world!")
        self.assertEqual(node2.to_html(), "Hello, world!")

    def test_repr(self):
        tag = "p"
        value = "Nolly is a cat"
        props = {"cats": "beautiful", "dogs": "ok"}

        node = LeafNode(tag, value, props)
        expected = f"LeafNode({tag}, {value}, {props})"
        self.assertEqual(node.__repr__(), expected)

    def expect_value_arg_error(self):
        with self.assertRaises(ValueError) as cm:
            LeafNode("p", "")

        excp = cm.exception
        self.assertEqual(excp.error_code, "All leaf nodes __must__ have a `value`")


class TestChildNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()
