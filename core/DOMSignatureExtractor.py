from selectolax.lexbor import LexborHTMLParser, LexborNode
from core.parameters import CONTAINER_TAGS, TERMINAL_BLOCKS, INLINE_TAGS, INTERACTIVE_TAGS


class DOMSignatureExtractor:
    def __init__(
            self,
            container_tags: set[str]    = CONTAINER_TAGS,
            terminal_blocks: set[str]   = TERMINAL_BLOCKS,
            inline_tags: set[str]       = INLINE_TAGS,
            interactive_tags: set[str]  = INTERACTIVE_TAGS,
            max_depth: int              = 9
        ) -> None:
        self.container_tags = container_tags
        self.terminal_blocks = terminal_blocks
        self.inline_tags = inline_tags
        self.interactive_tags = interactive_tags
        self.max_depth = max_depth

    def extract_signatures(self, body_node: LexborNode) -> list[str]:
        if not body_node:
            return []
        signatures: list[str]    = []
        current_path: list[str]  = []
        self._traverse(body_node, current_path, signatures)
        return signatures

    def _traverse(self, node: LexborNode, current_path: list[str], signatures: list[str]) -> None:
        if not node or node.tag == "-comment": return
        if node.tag in INTERACTIVE_TAGS:
            text = node.text(deep=True, separator=" ", strip=True, skip_empty=True)
            attrs_str = "["
            for attr, value in node.attributes.items():
                attrs_str += f"{attr}={value}, "
            attrs_str = attrs_str[:-2] + "]"

        if node.tag in TERMINAL_BLOCKS or self._is_leaf_block(node):
            text = node.text(deep=True, separator=" ", strip=True, skip_empty=True)
            text = self._normalize_whitespaces(text)

        # TODO:
        node_child = node.first_child
        while node_child is not None:
            self._traverse(node_child, current_path, signatures)
            node_child = node_child.next

    def _process_block(self, node: LexborNode):
        # TODO:
        pass

    def _is_leaf_block(self, node: LexborNode):
        """
        Returns True if this node is a terminal node (in other words, is not a container)
        Needed for <div> <section> etc, because they can contain text (in which we are interested in) or contain other elements (which are not relevant)

        Answers the question: does this block divide the page further or it already contains content
        """
        if not node:
            raise ValueError("Node cannot be `None`.")
        if isinstance(node, str):
            raise ValueError("Node must be LexborNode, not string")
        # TODO:
        node_child = node.first_child
        while node_child is not None:
            if node_child.tag in CONTAINER_TAGS or node_child.tag in TERMINAL_BLOCKS:
                return False
            node_child = node_child.next
        return True

    def _form_node_selector(self, node: LexborNode) -> str:
        # TODO:
        if not node or node.tag == "-text" or node.tag == "-document" or node.tag == "-comment":
            raise ValueError(f"Cannot form selector for: `{node.tag}`")

        selector = f"{node.tag}"
        validated_classes = self._split_and_validate_classes(node.attributes['class'])
        try:
            selector += f".{validated_classes[0]}"
            selector += f".{validated_classes[1]}"
        except IndexError:
            pass    # validated_classes doesn't have enough elements, skip

        if self._is_valid_id(node.id):
            selector += f"#{node.id}"
        elif not validated_classes:
            # selector += f":{self._make_node_id(node)}"
            # leave just tag
            pass
        return selector     # "div.class1_example.class2_example#id_example"

    def _make_node_id(self, node: LexborNode) -> str:
        return "test_stub"

    def _is_valid_id(self, id: str) -> bool:
        # TODO:
        return False

    def _split_and_validate_classes(self, class_field: str | None) -> list[str]:
        if not class_field:
            return []
        # TODO:
        return [class_field]    # ["example1", "example2"] or []

    def _normalize_whitespaces(self, text: str) -> str:
        # TODO:
        return text
