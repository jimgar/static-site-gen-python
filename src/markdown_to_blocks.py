def markdown_to_blocks(markdown):
    markdown = markdown.split("\n\n")
    markdown = [i.strip() for i in markdown]
    markdown = list(filter(lambda x: x != "", markdown))
    return markdown
