import pytest
from selectolax.lexbor import LexborHTMLParser
from core.DOMSignatureExtractor import DOMSignatureExtractor

def test_is_leaf_block_with_custom_tags():
    html = """
        <div class="price-row">
          <app-currency-icon></app-currency-icon>
          <span>500 zł</span>
        </div>
    """
    parser = LexborHTMLParser(html)
    exctractor = DOMSignatureExtractor()
    assert exctractor._is_leaf_block(parser.body.first_child)


def test_form_signature():
    pass

def test_is_leaf_block():
    pass


def test_form_node_selector():
    pass


def test_make_node_id():
    pass


@pytest.mark.parametrize("string, expected", [
    ("", False),
    (" ", False),
    ("\t\n", False),
    (None, False),
    ("main-content", True),
    ("sidebar", True),
    ("cart", True),
    ("item-1", True),
    ("step_2", True),
    (":r1:", False),
    (":R1:", False),
    (":r2a:", False),
    ("550e8400-e29b-41d4-a716-446655440000", False),
    ("modal_b1c2d3e4-f5a6-7b8c-9d0e-1f2a3b4c5d6e", False),
    ("ITEM-9B1DEB4D-3B7D-4BAD-9BDD-2B0D7B3DCB6D", False),
    ("cart_1727888645", False),
    ("1727888645", False),
    ("session-1727888645123", False),
    ("temp_a1b2c3d4e5f67890", False),
    ("65f3a1b0c9d8e7", False),
])
def test_is_valid_id(string, expected):
    exctractor = DOMSignatureExtractor()
    assert exctractor._is_valid_id(string) == expected

@pytest.mark.parametrize("string, expected", [
    (None, []),
    ("", []),
    (" ", []),
    (" card \t active \n ", ["card", "active"]),
    ("flex items-center justify-between p-4 text-sm", []),
    ("flex product-card items-center price text-red-500", ["product-card", "price"]),
    ("badge badge badge-primary", ["badge", "badge-primary"]),
    ("article-body summary", ["article-body", "summary"]),
    ("card post article summary highlight", ["card", "post"]),
])
def test_split_and_validate_classes(string, expected):
    exctractor = DOMSignatureExtractor()
    assert exctractor._split_and_validate_classes(string) == expected

@pytest.mark.parametrize("string, expected", [
    ("", False),
    (" ", False),
    ("_", False),
    ("a", False),
    ("this-is-a-very-very-very-very-long-class-name-exceeding-limit", False),
    (":r2:", False),
    ("p-4", False),
    ("h-12", False),
    ("w-full", False),
    ("gap-6", False),
    ("my-auto", False),
    ("flex", False),
    ("grid", False),
    ("inline-block", False),
    ("relative", False),
    ("hidden", False),
    ("text-red-500", False),
    ("font-bold", False),
    ("leading-tight", False),
    ("sm:hidden", False),
    ("md:flex", False),
    ("hover:bg-blue-500", False),
    ("dark:text-white", False),
    ("top-[10px]", False),
    ("w-[300px]", False),
    ("bg-[#f0f0f0]", False),
    ("sc-bdVaJa", False),
    ("gZfDmM", False),
    ("c18xTz", False),
    ("css-1q2w3e", False),
    ("card", True),
    ("price", True),
    ("btn-primary", True),
    ("active", True),
])
def test_is_valid_class(string, expected):
    exctractor = DOMSignatureExtractor()
    assert exctractor._is_valid_class(string) == expected


def test_normalize_whitespaces():
    exctractor = DOMSignatureExtractor()
    assert exctractor._normalize_whitespaces("\n\n     ") == ""
    assert exctractor._normalize_whitespaces("text\ntext") == "text text"
    assert exctractor._normalize_whitespaces("\n\n     ") == ""
    assert exctractor._normalize_whitespaces("\n\n     ") == ""
    assert exctractor._normalize_whitespaces("\n\n     ") == ""