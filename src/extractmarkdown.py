import re


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    if not matches:
        raise ValueError(
            f"No valid image syntax found in the text. Check for mistakes: '{text}'"
        )
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    if not matches:
        raise ValueError(
            f"No valid link syntax found in the text. Check for mistakes: '{text}'"
        )
    return matches
