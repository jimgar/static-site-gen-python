import unittest
from extractmarkdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        res = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expt = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(res, expt)

    def test_extract_markdown_images_no_alt(self):
        res = extract_markdown_images(
            "Blah blah words ![](https://internet.com/image.piss)"
        )
        expt = [("", "https://internet.com/image.piss")]
        self.assertListEqual(res, expt)

    def test_extract_markdown_images_no_url(self):
        res = extract_markdown_images("Blah blah words ![image alt text]()")
        expt = [("image alt text", "")]
        self.assertListEqual(res, expt)

    def test_extract_markdown_images_no_url_no_alt(self):
        res = extract_markdown_images("Blah blah words ![]()")
        expt = [("", "")]
        self.assertListEqual(res, expt)

    def test_multiple_images_in_text(self):
        res = extract_markdown_images(
            "Blah blah words ![alt text 1](https://internet.com/image.piss) and more stuff with ![some other image](https://dogs.cats.cool) here"
        )
        expt = [
            ("alt text 1", "https://internet.com/image.piss"),
            ("some other image", "https://dogs.cats.cool"),
        ]
        self.assertListEqual(res, expt)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        res = extract_markdown_links(
            "This is text with a [link](https://surf-the-net.web) in it"
        )
        expt = [("link", "https://surf-the-net.web")]
        self.assertListEqual(res, expt)

    def test_extract_markdown_links_no_link(self):
        res = extract_markdown_links("Blah blah words [](https://internet.com)")
        expt = [("", "https://internet.com")]
        self.assertListEqual(res, expt)

    def test_extract_markdown_links_no_url(self):
        res = extract_markdown_links("Blah blah words [link text]()")
        expt = [("link text", "")]
        self.assertListEqual(res, expt)

    def test_extract_markdown_links_no_url_no_link(self):
        res = extract_markdown_links("Blah blah words []()")
        expt = [("", "")]
        self.assertListEqual(res, expt)

    def test_multiple_links_in_text(self):
        res = extract_markdown_links(
            "Blah blah words [link text 1](https://internet.com) and more stuff with [some other link](https://dogs.cats.cool) here"
        )
        expt = [
            ("link text 1", "https://internet.com"),
            ("some other link", "https://dogs.cats.cool"),
        ]
        self.assertListEqual(res, expt)
