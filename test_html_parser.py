from html_parser import BaseParser


def test_should_pass_html_through_pipeline_unaffected_if_no_transforms():
    raw_html = """
    <html>
    <head>
        <title>Hello World</title>
    </head>
    <body>
        <p claas="foo">Hello World</p>
    </body>
    </html>
    """

    buffer = []
    parser = BaseParser(buffer)
    parser.feed(raw_html)
    assert ''.join(buffer) == raw_html


def test_should_preserve_entity_ref_and_char_ref_in_html():
    raw_html = """
        <html>
        <body>
            <p>&quot; Hello World &quot;</p>
            <p>&#169; copyright HPYC</p> 
        </body>
        </html>
        """

    buffer = []
    parser = BaseParser(buffer)
    parser.feed(raw_html)
    assert ''.join(buffer) == raw_html


def test_should_simply_pass_on_captured_tag():
    raw_html = """
        <html>
        <body>
           <foo>foobar</foo>
        </body>
        </html>
        """

    buffer = []
    parser = BaseParser(buffer, "foo")
    parser.feed(raw_html)
    assert ''.join(buffer) == raw_html


def test_not_care_if_tag_is_missing():
    raw_html = """
        <html>
        <body>
           <not-foo>foobar</not-foo>
        </body>
        </html>
        """

    buffer = []
    parser = BaseParser(buffer, "foo")
    parser.feed(raw_html)
    assert ''.join(buffer) == raw_html


def test_subclass_can_override_handle_captured():
    class TestParser(BaseParser):
        def __init__(self, content_buffer):
            BaseParser.__init__(self, content_buffer, ['foo'])

        def handle_captured(self, tag_name, captured):
            self.content_buffer.extend(''.join(captured).upper())

    raw_html = """
        <html>
        <body>
           <foo>foobar</foo>
        </body>
        </html>
        """

    expected_html = """
        <html>
        <body>
           FOOBAR
        </body>
        </html>
        """

    buffer = []
    parser = TestParser(buffer)
    parser.feed(raw_html)
    assert ''.join(buffer) == expected_html
