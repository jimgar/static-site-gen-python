import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    # Prepare HTML
    html_string = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    # Write out HTML
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        if Path(dir_path_content).suffix == ".md":
            html_dest_path = dest_dir_path.replace(".md", ".html")
            generate_page(dir_path_content, template_path, html_dest_path)
        return

    all_dir = os.listdir(dir_path_content)
    print(f"all_dir: {all_dir}")

    if len(all_dir) == 0:
        return

    for path in all_dir:
        print(f"path: {path}")
        new_dest_path = os.path.join(dest_dir_path, path)
        current_path = os.path.join(dir_path_content, path)
        print(f"current path: {current_path}")
        print(f"new path: {new_dest_path}")
        generate_pages_recursive(current_path, template_path, new_dest_path)
