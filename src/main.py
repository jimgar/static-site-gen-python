from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
from splitnodes import split_nodes_delimiter, split_nodes_image


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

    print("\n\n---- split_nodes_image ----\n")
    # print(split_nodes_image([]))

    img_node1 = TextNode(
        "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )

    img_node2 = TextNode(
        "![Alt text for boot.dev](https://www.boot.dev) and that's it!",
        TextType.TEXT,
    )
    print(split_nodes_image([img_node1, img_node2]))

    img_node3 = TextNode("![Just alt text](http://andalink.com)", TextType.TEXT)
    print(split_nodes_image([img_node3]))

    print("\n\n---- no valid image format ----\n")
    img_node4 = TextNode("![Just alt text(http://andalink.com)", TextType.TEXT)
    print(split_nodes_image([img_node4]))

    print("\n\n---- no text at all ----\n")
    img_node5 = TextNode("", TextType.TEXT)
    print(split_nodes_image([img_node5]))
    # print(split_nodes_image([]))


if __name__ == "__main__":
    main()
