from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images, extract_markdown_links


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


def split_nodes_image(old_nodes):
    if not old_nodes:
        raise ValueError("old_nodes should be a list of nodes but is empty/None")

    new_nodes = []
    for old_n in old_nodes:
        if old_n.text_type != TextType.TEXT:
            new_nodes.append(old_n)
            continue

        if not old_n.text:
            continue

        images = extract_markdown_images(old_n.text)

        if not images:
            # At this point we know there must be text, but it doesn't contain any valid image markdown.
            new_nodes.append(old_n)
            continue

        pieces = []
        text = old_n.text
        for image in images:
            if text == "":
                continue
            image_md = f"![{image[0]}]({image[1]})"
            text_split = text.split(image_md, 1)
            # Capture text before the image, if there was any
            if text_split[0]:
                pieces.append(TextNode(text_split[0], TextType.TEXT))
            # Capture the image
            pieces.append(TextNode(image[0], TextType.IMAGE, image[1]))
            # Only the remaining text need to be taken forward
            text = text_split[1]

        # Capture any image-less text that is left over
        if text:
            pieces.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(pieces)

    return new_nodes


def split_nodes_link(old_nodes):
    if not old_nodes:
        raise ValueError("old_nodes should be a list of nodes but is empty/None")

    new_nodes = []
    for old_n in old_nodes:
        if old_n.text_type != TextType.TEXT:
            new_nodes.append(old_n)
            continue

        if not old_n.text:
            continue

        links = extract_markdown_links(old_n.text)

        if not links:
            # At this point we know there must be text, but it doesn't contain any valid link markdown.
            new_nodes.append(old_n)
            continue

        pieces = []
        text = old_n.text
        for link in links:
            if text == "":
                continue
            link_md = f"[{link[0]}]({link[1]})"
            text_split = text.split(link_md, 1)
            # Capture text before the link, if there was any
            if text_split[0]:
                pieces.append(TextNode(text_split[0], TextType.TEXT))
            # Capture the link
            pieces.append(TextNode(link[0], TextType.LINK, link[1]))
            # Only the remaining text need to be taken forward
            text = text_split[1]

        # Capture any link-less text that is left over
        if text:
            pieces.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(pieces)

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)

    bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    images = split_nodes_image(code)
    links = split_nodes_link(images)

    return links
