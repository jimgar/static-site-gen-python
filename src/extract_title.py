def extract_title(markdown):
    h1_pattern = "# "
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith(h1_pattern):
            return line.lstrip(h1_pattern).strip()

    raise Exception("No h1 header")
