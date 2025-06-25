from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
from splitnodes import split_nodes_delimiter


def main():
    node = TextNode("This is some anchor text", TextType.TEXT, "blahakljsdff")
    print(node)

    leaf_node = LeafNode("br", "Text to go between the tags")
    print(leaf_node)

    parent_node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    print(parent_node.to_html())

    n1 = TextNode("This is text with a `code block` word", TextType.TEXT)
    n2 = TextNode("This is `code text` with a `code block` word", TextType.TEXT)
    n3 = TextNode("This is text with a code block word", TextType.TEXT)
    n4 = TextNode("", TextType.TEXT)
    n5 = TextNode("Some **donkus**", TextType.TEXT)
    new_nodes = split_nodes_delimiter([n1, n2, n3, n5, n4], "`", TextType.CODE)
    for i in new_nodes:
        print(i)


if __name__ == "__main__":
    main()
