from selectolax.lexbor import LexborHTMLParser

# Docs: https://selectolax.readthedocs.io/en/latest/examples.html#advanced-selectors

DEFAULT_TAGS_BLACKLIST = [
    "head",
    "style",
    "script",
    "template",
    "svg",
    "iframe",
    "noscript",
    "canvas",
    "audio",
    "video",
]

DEFAULT_NOISE_SELECTORS: list[str] = [
    'input[type="hidden"]',
    "[hidden]",
    '[aria-hidden="true"]',
    '[style*="display:none"]',
    '[style*="display: none"]',
    '[id*="cookie" i]',
    '[class*="cookie" i]',
    '[id*="consent" i]',
    '[class*="consent" i]',
]

def sanitize_html(raw_html: str) -> LexborHTMLParser:
    parser = LexborHTMLParser(raw_html)

    for tag in DEFAULT_TAGS_BLACKLIST:
        for node in parser.tags(tag):
            node.decompose()

    for selector in DEFAULT_NOISE_SELECTORS:
        for node in parser.css(selector):
            node.decompose()

    # parser.unwrap_tags(["strong"])
    return parser


def normalize_whitespaces(text: str) -> str:
    # text.replace
    return ""
