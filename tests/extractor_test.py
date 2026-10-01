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
