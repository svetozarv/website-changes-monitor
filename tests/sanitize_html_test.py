import pytest
from core.utils import sanitize_html


def test_sanitize_html():
    dirty_html = """
    <div id="wrapper">
        <p>Meaningful text</p>
        <script>console.log("tracker");</script>
        <div class="Cookie-Banner">
            <button>Accept</button>
        </div>
        <input type="hidden" name="token" value="dynamic_xyz" />
    </div>
    """

    clean_parser = sanitize_html(dirty_html)
    print(clean_parser)
    assert clean_parser.css("script") == []
    assert clean_parser.css(".Cookie-Banner") == []
    assert clean_parser.css('input[type="hidden"]') == []


def test_removes_blacklisted_tags():
    dirty_html = """
    <div>
        <p>Legitimate text</p>
        <script>alert('xss')</script>
        <style>body { color: red; }</style>
        <svg><path d="M0 0"/></svg>
        <iframe>src="http://tracker.com"</iframe>
    </div>
    """
    tree = sanitize_html(dirty_html)

    assert tree.css("script") == []
    assert tree.css("style") == []
    assert tree.css("svg") == []
    assert tree.css("iframe") == []

    p_tags = tree.css("p")
    assert len(p_tags) == 1
    assert p_tags[0].text() == "Legitimate text"


def test_removes_hidden_inputs():
    dirty_html = """
    <form>
        <input type="hidden" name="csrf_token" value="abc123dynamic" />
        <input type="text" name="username" value="john" />
    </form>
    """
    tree = sanitize_html(dirty_html)

    assert tree.css('input[type="hidden"]') == []
    visible_inputs = tree.css('input[type="text"]')
    assert len(visible_inputs) == 1
    assert visible_inputs[0].attributes.get("name") == "username"


@pytest.mark.parametrize("payload", [
    "<script>alert(1)</script>",
    "<style>.body { display: none; }</style>",
    "<noscript><meta http-equiv='refresh' content='0'></noscript>",
])
def test_noise_tags_parameterized(payload):
    input_html = f"<div>Content before {payload} Content after</div>"
    tree = sanitize_html(input_html)

    assert payload not in tree.body.text()
    assert "Content before" in tree.body.text()
    assert "Content after" in tree.body.text()
