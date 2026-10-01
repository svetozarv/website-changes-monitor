
CONTAINER_TAGS = {
    "div",
    "section",
    "article",
    "main",
    "aside",
    "nav",
    "header",
    "footer",
    "form",
    "ul",
    "ol",
    "table",
    "tbody",
    "tr",
    "thead",
    "tfoot",
    "figure",
    "dl",
    "fieldset",
    "details",
}

# These are the leaf nodes that represent a unit of information.
# All of their children belong to them and together make up ONE sentence/signature
# use deep(true) on them
# do not traverse deeper
TERMINAL_BLOCKS = {
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "li",
    "td",
    "th",
    "blockquote",
    "dt",
    "dd",
    "pre",
    "figcaption",
    "summary",
}

# Always included in the signature, no matter what
# additional attributes are preserved (links etc)
INTERACTIVE_TAGS = {
    "button",
    "a",
    "input",
    "select",
    "textarea",
    "img",
}

TRACKED_ATTRIBUTES = {
    "href",
    "src",
    "disabled",
    "readonly",
    "checked",
    "value",
    "title",
    "alt",
}

# Tags that are essentially part of the text
INLINE_TAGS = {
    "span",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "s",
    "small",
    "del",
    "ins",
    "mark",
    "sub",
    "sup",
    "label",
    "code",
    "time",
    "abbr",
    "cite",
    "q",
    "kbd",
    "var",
    "samp",
    "br",
    "wbr",
}
