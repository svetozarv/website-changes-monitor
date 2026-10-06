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


def test_is_valid_id():
    exctractor = DOMSignatureExtractor()
    assert not exctractor._is_valid_id("")
    assert not exctractor._is_valid_id(" ")
    assert not exctractor._is_valid_id("\t\n")
    assert not exctractor._is_valid_id(None)

    assert exctractor._is_valid_id("main-content")
    assert exctractor._is_valid_id("sidebar")
    assert exctractor._is_valid_id("cart")
    assert exctractor._is_valid_id("item-1")
    assert exctractor._is_valid_id("step_2")

    assert not exctractor._is_valid_id(":r1:")
    assert not exctractor._is_valid_id(":R1:")
    assert not exctractor._is_valid_id(":r2a:")

    assert not exctractor._is_valid_id("550e8400-e29b-41d4-a716-446655440000")
    assert not exctractor._is_valid_id("modal_b1c2d3e4-f5a6-7b8c-9d0e-1f2a3b4c5d6e")
    assert not exctractor._is_valid_id("ITEM-9B1DEB4D-3B7D-4BAD-9BDD-2B0D7B3DCB6D")
    assert not exctractor._is_valid_id("cart_1727888645")
    assert not exctractor._is_valid_id("1727888645")
    assert not exctractor._is_valid_id("session-1727888645123")
    assert not exctractor._is_valid_id("temp_a1b2c3d4e5f67890")
    assert not exctractor._is_valid_id("65f3a1b0c9d8e7")


def test_split_and_validate_classes():
    exctractor = DOMSignatureExtractor()
    assert exctractor._split_and_validate_classes(None) == []
    assert exctractor._split_and_validate_classes("") == []
    assert exctractor._split_and_validate_classes(" ") == []
    assert exctractor._split_and_validate_classes(" card \t active \n ") == ["card", "active"]
    assert exctractor._split_and_validate_classes("flex items-center justify-between p-4 text-sm") == []
    assert exctractor._split_and_validate_classes("flex product-card items-center price text-red-500") == ["product-card", "price"]
    assert exctractor._split_and_validate_classes("badge badge badge-primary") == ["badge", "badge-primary"]
    assert exctractor._split_and_validate_classes("article-body summary") == ["article-body", "summary"]
    assert exctractor._split_and_validate_classes("card post article summary highlight") == ["card", "post"]


def test_is_valid_class():
    exctractor = DOMSignatureExtractor()
    assert not exctractor._is_valid_class("")
    assert not exctractor._is_valid_class(" ")
    assert not exctractor._is_valid_class("_")
    assert not exctractor._is_valid_class("a")
    assert not exctractor._is_valid_class("this-is-a-very-very-very-very-long-class-name-exceeding-limit")

    assert not exctractor._is_valid_class(":r2:")
    assert not exctractor._is_valid_class("p-4")
    assert not exctractor._is_valid_class("h-12")
    assert not exctractor._is_valid_class("w-full")
    assert not exctractor._is_valid_class("gap-6")
    assert not exctractor._is_valid_class("my-auto")

    assert not exctractor._is_valid_class("flex")
    assert not exctractor._is_valid_class("grid")
    assert not exctractor._is_valid_class("inline-block")
    assert not exctractor._is_valid_class("relative")
    assert not exctractor._is_valid_class("hidden")

    assert not exctractor._is_valid_class("text-red-500")
    assert not exctractor._is_valid_class("font-bold")
    assert not exctractor._is_valid_class("leading-tight")
    assert not exctractor._is_valid_class("sm:hidden")
    assert not exctractor._is_valid_class("md:flex")
    assert not exctractor._is_valid_class("hover:bg-blue-500")
    assert not exctractor._is_valid_class("dark:text-white")
    assert not exctractor._is_valid_class("top-[10px]")
    assert not exctractor._is_valid_class("w-[300px]")
    assert not exctractor._is_valid_class("bg-[#f0f0f0]")
    assert not exctractor._is_valid_class("sc-bdVaJa")
    assert not exctractor._is_valid_class("gZfDmM")
    assert not exctractor._is_valid_class("c18xTz")
    assert not exctractor._is_valid_class("css-1q2w3e")

    assert exctractor._is_valid_class("card")
    assert exctractor._is_valid_class("price")
    assert exctractor._is_valid_class("btn-primary")
    assert exctractor._is_valid_class("active")


def test_normalize_whitespaces():
    exctractor = DOMSignatureExtractor()
    assert exctractor._normalize_whitespaces("\n\n     ") == ""
    assert exctractor._normalize_whitespaces("text\ntext") == "text text"
    assert exctractor._normalize_whitespaces("\n\n     ") == ""
    assert exctractor._normalize_whitespaces("\n\n     ") == ""
    assert exctractor._normalize_whitespaces("\n\n     ") == ""