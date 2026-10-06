# TODO: add ability to modify this during runtime
# TODO: make it customizable for each webpage

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


# Exact matches for standalone layout utility CSS keywords
UTILITY_EXACT_MATCHES: set[str] = {
    "flex",
    "inline-flex",
    "grid",
    "hidden",
    "block",
    "inline-block",
    "relative",
    "absolute",
    "fixed",
    "sticky",
    "container",
    "truncate",
}


UTILITY_PREFIXES: tuple[str, ...] = (
    "p-", "px-", "py-", "pt-", "pb-", "pl-", "pr-",
    "m-", "mx-", "my-", "mt-", "mb-", "ml-", "mr-",
    "w-", "h-", "min-w-", "max-w-", "min-h-", "max-h-",
    "gap-", "space-", "col-", "row-",
    "items-", "justify-", "content-", "self-", "place-",        # Flexbox and  Grid alignment
    "text-", "font-", "leading-", "tracking-", "bg-", "border-", "rounded-",
    "transition-", "duration-", "shadow-", "opacity-", "z-",
)

BUNDLER_PREFIXES: tuple[str, ...] = ("sc-", "css-")
