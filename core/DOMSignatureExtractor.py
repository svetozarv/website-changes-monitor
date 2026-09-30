from selectolax.lexbor import LexborHTMLParser
# div.card > button.btn-buy > span (tag.class)

TERMINAL_BLOCKS = [
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "li",
    "tr",
    "td",
    "article",
    "section",
    "div",
    "blockquote",
    "header",
    "footer",
    "nav"
]

# Tags that are essentially part of the text
INLINE_TAGS = [
    "span",
    "strong",
    "b",
    "em",
    "i",
    "small",
    "del",
    "ins",
    "mark",
    "sub",
    "sup",
    "label"
]


class DOMSignatureExtractor:
    def __init__(self):
        pass

    def extract_signatures(self):
        pass

    def _traverse(self):
        pass

    def _process_block(self):
        pass

    def _is_content_leaf(self, node):
        return "stab"

    def _build_breadcrumb(self):
        pass
