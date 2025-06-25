from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        raise ValueError("old_nodes should be a list of nodes but is empty/None")

    new_nodes = []
    for old_n in old_nodes:
        if old_n.text_type.value != "text":
            new_nodes.append(old_n)
            continue

        old_n_split = old_n.text.split(delimiter)

        if len(old_n_split) % 2 == 0:
            raise Exception(
                f"Odd number of delimiter ({delimiter}) found. Markdown delimiters should come in pairs, e.g. `inline code` or **bold text**"
            )

        # There **is** a string, but it didn't contain the delimiter. Must just be plain text.
        if len(old_n_split) == 1 and old_n_split[0]:
            new_nodes.append(TextNode(old_n.text, TextType.TEXT))
            continue

        pieces = []
        for idx, piece in enumerate(old_n_split):
            if piece == "":
                continue

            if idx % 2 == 0:
                pieces.append(TextNode(piece, TextType.TEXT))
            else:
                pieces.append(TextNode(piece, text_type))

        new_nodes.extend(pieces)

    return new_nodes
