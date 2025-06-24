from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode


def main():
    node = TextNode("This is some anchor text", TextType.NORMAL, "blahakljsdff")
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


if __name__ == "__main__":
    main()
