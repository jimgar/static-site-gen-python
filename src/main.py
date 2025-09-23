from copy_content import copy_content
from generate_page import generate_pages_recursive


def main():
    copy_content("static", "public")
    generate_pages_recursive("content", "template.html", "public")


main()
