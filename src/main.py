import sys
from copy_content import copy_content
from generate_page import generate_pages_recursive


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_content("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
