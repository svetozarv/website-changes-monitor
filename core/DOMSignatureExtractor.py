from selectolax.lexbor import LexborHTMLParser, LexborNode
from core.parameters import CONTAINER_TAGS, TERMINAL_BLOCKS, INLINE_TAGS, INTERACTIVE_TAGS, TRACKED_ATTRIBUTES
import re

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
        self._traverse(body_node, current_path, signatures)     # the current_path and signatures are modified in-place though the entire call stack
        return signatures

    def _traverse(self, node: LexborNode, current_path: list[str], signatures: list[str]) -> None:
        if not node or node.tag == "-comment": return
        if node.tag in INTERACTIVE_TAGS:
            text = node.text(deep=True, separator=" ", strip=True, skip_empty=True)

            # form node signature: collect tracked attributes
            # ex. `a[href=example.com]``
            attrs_str = "["
            for attr, value in node.attributes.items():
                if attr not in TRACKED_ATTRIBUTES: continue
                attrs_str += f"{attr}={value}, "
            attrs_str = attrs_str[:-2] + "]"
            node_selector = f"{node.tag}{attrs_str}"
            current_path.append(node_selector)

            signatures.append(self._form_signature(current_path))

            current_path.pop()
            self._traverse(node.next, current_path, signatures)  # stop  kids traversal go to neighbour
            return

        if node.tag in TERMINAL_BLOCKS or self._is_leaf_block(node):
            text = node.text(deep=True, separator=" ", strip=True, skip_empty=True)
            text = self._normalize_whitespaces(text)
            if not text: return
            node_selector = self._form_node_selector(node)
            current_path.append(node_selector)
            signatures.append(self._form_signature(current_path))
            current_path.pop()
            self._traverse(node.next, current_path, signatures)  # stop  kids traversal go to neighbour
            return

        if node.tag in CONTAINER_TAGS:
            added_selector = False

            node_selector = self._form_node_selector(node)
            if node_selector != node.tag:
                current_path.append(node_selector)
                added_selector = True
            self._traverse_node_children(node, current_path, signatures)

            if added_selector:
                current_path.pop()
            signatures.append(self._form_signature(current_path))

    def _form_signature(self, current_path: list[str]) -> str:
        return " > ".join(current_path)

    def _traverse_node_children(self, node: LexborNode, current_path: list[str], signatures: list[str]) -> None:
        node_child = node.first_child
        while node_child is not None:
            self._traverse(node_child, current_path, signatures)
            node_child = node_child.next

    # TODO: implement
    def _process_block(self, node: LexborNode):
        pass

    def _is_leaf_block(self, node: LexborNode) -> bool:
        """
        Returns True if this node is a terminal node (in other words, is not a container)
        Needed for <div> <section> etc, because they can contain text (in which we are interested in) or contain other elements (which are not relevant)

        Answers the question: does this block divide the page further or it already contains content
        """
        if not node:
            raise ValueError("Node cannot be `None`.")
        if isinstance(node, str):
            raise ValueError("Node must be LexborNode, not string")

        node_child = node.first_child
        while node_child is not None:
            if node_child.tag in CONTAINER_TAGS or node_child.tag in TERMINAL_BLOCKS:
                return False
            node_child = node_child.next
        return True

    # TODO: test
    def _form_node_selector(self, node: LexborNode) -> str:
        """
        Forms node selector.

        Examples:
            - `div.class1_example.class2_example#id_example`
                - if 2 or more classes are valid.
            ---
            - `div.class_example#id_example`
                - if only one class is valid.
            ---
            - `div#id_example`
                - if no valid classes.
            ---
            - `div`
                - if neither classes nor id are valid.
        """
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
            # leave just tag for now
            pass
        return selector

    def _make_node_id(self, node: LexborNode) -> str:
        """
        Make a unique node selector identifier, so the element in a breadcrump
        can be recognized as separate or related text in comparison to other breadcrumbs.

        Example:
        `div > element#(first_element) > Relevant information`
        `div > element#(second_element) > Unavailable`
        """
        return "test_stub"

    # TODO: test
    def _is_valid_id(self, id: str | None) -> bool:
        """
        Checks if id was autogenerated and looks like timestap, hash, UUID etc.
        """
        if not id and not id.strip():
            return False

        id = id.strip()

        if re.search(r":r.*:", id):     # autogenerated by React/Next.js
            return False

        if re.search(r"[0-9a-fA-f]{8}-[0-9a-fA-f]{4}-[0-9a-fA-f]{4}-[0-9a-fA-f]{4}-[0-9a-fA-f]{12}", id):   # UUID / GUID
            return False

        if re.search(r"[_-]?\b1\d{9}(?:\d{3})?\b", id): # Unix timestaps
            return False

        if re.search(r"[-_]?[0-9a-fA-F]{12,}\b", id):   # hashes (MD5)
            return False

        return True

    # TODO: test
    def _split_and_validate_classes(self, class_fields: str | None) -> list[str]:
        if not class_fields:
            return []

        valid_classes = []
        for class_field in class_fields:
            if self._is_valid_class(class_field):
                valid_classes.append(class_field)
            if len(valid_classes) == 2:
                break

        return valid_classes    # ["example1", "example2"] or []

    # TODO: test
    def _is_valid_class(self, class_field: str) -> bool:
        """
        Checks if class was autogenerated by Tailwind or Bootstrap or it looks like hash.
        """
        if not class_field and not class_field.strip():
            return False

        if re.search(r"(sm:|md:|lg:|hover:|focus:)", class_field):
            return False

        if re.search(r"(flex-|grid-|p-|m-|w-|h-|bg-|text-|col-|row-)", class_field):
            return False

        if re.search(r"^\w{7,}", class_field):
            return False

        return True

    # TODO: test
    def _normalize_whitespaces(self, text: str) -> str:
        """
        Replaces multiple spaces, newlines and no-break space with a single space.
        """
        return re.sub(r"(\s+|&nbsp;|\\xa0)", " ", text.strip())
