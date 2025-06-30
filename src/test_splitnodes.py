import unittest

from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_straightforward_cases(self):
        n1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        res1 = split_nodes_delimiter([n1], "`", TextType.CODE)
        expt1 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        n2 = TextNode("A **bolded** word.", TextType.TEXT)
        res2 = split_nodes_delimiter([n2], "**", TextType.BOLD)
        expt2 = [
            TextNode("A ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
        ]

        n3 = TextNode("An _italicised_ word.", TextType.TEXT)
        res3 = split_nodes_delimiter([n3], "_", TextType.ITALIC)
        expt3 = [
            TextNode("An ", TextType.TEXT),
            TextNode("italicised", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
        ]

        self.assertEqual(res1, expt1)
        self.assertEqual(res2, expt2)
        self.assertEqual(res3, expt3)

    def test_empty_input(self):
        n = TextNode("", TextType.TEXT)
        res = split_nodes_delimiter([n], "_", TextType.ITALIC)
        expt = []

        self.assertEqual(res, expt)

    def test_nested(self):
        n = TextNode("Well **that's just _terrible_**!", TextType.TEXT)

        res1 = split_nodes_delimiter([n], "_", TextType.ITALIC)
        expt1 = [
            TextNode("Well **that's just ", TextType.TEXT),
            TextNode("terrible", TextType.ITALIC),
            TextNode("**!", TextType.TEXT),
        ]

        res2 = split_nodes_delimiter([n], "**", TextType.BOLD)
        expt2 = [
            TextNode("Well ", TextType.TEXT),
            TextNode("that's just _terrible_", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]

        self.assertEqual(res1, expt1)
        self.assertEqual(res2, expt2)

    def test_non_text(self):
        n = TextNode("Well **that's just _terrible_**!", TextType.CODE)

        res = split_nodes_delimiter([n], "**", TextType.BOLD)
        expt = [TextNode("Well **that's just _terrible_**!", TextType.CODE)]

        self.assertEqual(res, expt)

    def test_wrong_delimiter_for_text(self):
        n = TextNode("Well **that's just _terrible_**!", TextType.TEXT)

        res = split_nodes_delimiter([n], "`", TextType.CODE)
        expt = [TextNode("Well **that's just _terrible_**!", TextType.TEXT)]

        self.assertEqual(res, expt)

    def test_unmatched_delim_throws_error(self):
        n = TextNode("Somethin' just ain't **right here", TextType.TEXT)

        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([n], "**", TextType.BOLD)

        excp = cm.exception
        self.assertEqual(
            excp.__str__(),
            "Odd number of delimiter (**) found. Markdown delimiters should come in pairs, e.g. `inline code` or **bold text**",
        )


class TestSplitNodesImage(unittest.TestCase):
    # -- Two images in some text --
    two_images_one_text = TextNode(
        "This is an image for boot.dev ![A photo of Boots the bear](https://www.boot.dev/boots.jpg) and the boot.dev YouTube channel ![A YouTube video thumbnail](https://www.boot.dev/youtube.png)",
        TextType.TEXT,
    )

    two_images_one_text_expected = [
        TextNode("This is an image for boot.dev ", TextType.TEXT),
        TextNode(
            "A photo of Boots the bear",
            TextType.IMAGE,
            "https://www.boot.dev/boots.jpg",
        ),
        TextNode(" and the boot.dev YouTube channel ", TextType.TEXT),
        TextNode(
            "A YouTube video thumbnail",
            TextType.IMAGE,
            "https://www.boot.dev/youtube.png",
        ),
    ]

    two_images_one_text_result = split_nodes_image([two_images_one_text])

    # -- Single image with some text --
    single_image_and_text = TextNode(
        "![Alt text for boot.dev](https://www.boot.dev/image.tiff) and that's it!",
        TextType.TEXT,
    )

    single_image_and_text_expected = [
        TextNode(
            "Alt text for boot.dev", TextType.IMAGE, "https://www.boot.dev/image.tiff"
        ),
        TextNode(" and that's it!", TextType.TEXT),
    ]

    single_image_and_text_result = split_nodes_image([single_image_and_text])

    # -- Just image markdown --
    just_image_markdown = TextNode(
        "![All this contains is image markdown](https://www.boot.dev/image.tiff)",
        TextType.TEXT,
    )

    just_image_markdown_expected = [
        TextNode(
            "All this contains is image markdown",
            TextType.IMAGE,
            "https://www.boot.dev/image.tiff",
        ),
    ]

    just_image_markdown_result = split_nodes_image([just_image_markdown])

    def test_straightforward_cases(self):
        self.assertListEqual(
            self.two_images_one_text_result, self.two_images_one_text_expected
        )

        self.assertListEqual(
            self.single_image_and_text_result, self.single_image_and_text_expected
        )

        # Two straightforward ones together
        exp = self.two_images_one_text_expected.copy()
        exp.extend(self.single_image_and_text_expected)
        res = split_nodes_image([self.two_images_one_text, self.single_image_and_text])
        self.assertListEqual(res, exp)

        self.assertListEqual(
            self.just_image_markdown_result, self.just_image_markdown_expected
        )

    malformed = TextNode(
        "![Just alt text(http://andalink.com/cowboy.svg)", TextType.TEXT
    )
    malformed_res = split_nodes_image([malformed])

    def test_malformed_image(self):
        self.assertListEqual(self.malformed_res, [self.malformed])

    no_text = TextNode("", TextType.TEXT)
    no_text_res = split_nodes_image([no_text])

    def test_no_text_at_all(self):
        self.assertListEqual([], self.no_text_res)

    def test_mixture(self):
        res = split_nodes_image(
            [
                self.two_images_one_text,
                self.malformed,
                self.no_text,
                self.single_image_and_text,
                self.just_image_markdown,
            ]
        )
        exp = (
            self.two_images_one_text_expected
            + [self.malformed]
            + []
            + self.single_image_and_text_expected
            + self.just_image_markdown_expected
        )
        self.assertListEqual(res, exp)


class TestSplitNodesLink(unittest.TestCase):
    # -- Two links in some text --
    two_links_one_text = TextNode(
        "This is a link to [boot.dev](https://www.boot.dev) and the boot.dev [YouTube channel](https://www.youtube.com/@poop.dev)",
        TextType.TEXT,
    )

    two_links_one_text_expected = [
        TextNode("This is a link to ", TextType.TEXT),
        TextNode(
            "boot.dev",
            TextType.LINK,
            "https://www.boot.dev",
        ),
        TextNode(" and the boot.dev ", TextType.TEXT),
        TextNode(
            "YouTube channel",
            TextType.LINK,
            "https://www.youtube.com/@poop.dev",
        ),
    ]

    two_links_one_text_result = split_nodes_link([two_links_one_text])

    # -- Single link with some text --
    single_link_and_text = TextNode(
        "[Text for boot.dev](https://www.boot.dev) and that's it!",
        TextType.TEXT,
    )

    single_link_and_text_expected = [
        TextNode("Text for boot.dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and that's it!", TextType.TEXT),
    ]

    single_link_and_text_result = split_nodes_link([single_link_and_text])

    # -- Just image markdown --
    just_link_markdown = TextNode(
        "[All this contains is link markdown](https://www.boot.dev)",
        TextType.TEXT,
    )

    just_link_markdown_expected = [
        TextNode(
            "All this contains is link markdown",
            TextType.LINK,
            "https://www.boot.dev",
        ),
    ]

    just_link_markdown_result = split_nodes_link([just_link_markdown])

    def test_straightforward_cases(self):
        self.assertListEqual(
            self.two_links_one_text_result, self.two_links_one_text_expected
        )

        self.assertListEqual(
            self.single_link_and_text_result, self.single_link_and_text_expected
        )

        # Two straightforward ones together
        exp = self.two_links_one_text_expected.copy()
        exp.extend(self.single_link_and_text_expected)
        res = split_nodes_link([self.two_links_one_text, self.single_link_and_text])
        self.assertListEqual(res, exp)

        self.assertListEqual(
            self.just_link_markdown_result, self.just_link_markdown_expected
        )

    malformed = TextNode("[Just link text(http://andalink.com)", TextType.TEXT)
    malformed_res = split_nodes_link([malformed])

    def test_malformed_image(self):
        self.assertListEqual(self.malformed_res, [self.malformed])

    no_text = TextNode("", TextType.TEXT)
    no_text_res = split_nodes_link([no_text])

    def test_no_text_at_all(self):
        self.assertListEqual([], self.no_text_res)

    def test_mixture(self):
        res = split_nodes_link(
            [
                self.two_links_one_text,
                self.malformed,
                self.no_text,
                self.single_link_and_text,
                self.just_link_markdown,
            ]
        )
        exp = (
            self.two_links_one_text_expected
            + [self.malformed]
            + []
            + self.single_link_and_text_expected
            + self.just_link_markdown_expected
        )
        self.assertListEqual(res, exp)
