from html_pipeline import BaseParser
from transformer import Transform


# some simple transformers
class FooTransform(Transform):

    def __init__(self, ):
        self.outer_tag = "foo-content"

    def transform(self, nodes: list) -> str:
        result = ''
        for node in nodes:
            if node.tag == 'p':
                result += '<div>' + str(node.text).upper() + '</div>'
        return result


class BarTransform(Transform):

    def __init__(self, ):
        self.outer_tag = "bar-content"

    def transform(self, nodes: list) -> str:
        result = ''
        for node in nodes:
            if node.tag == 'header':
                result += '<h1>' + str(node.text).upper() + '</h1>'
        return result


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


def test_should_apply_single_transformer_to_html():
    raw_html = """
         <html>
         <body>
             <foo-content><p>Foo</p></foo-content>
         </body>
         </html>"""

    output_html = """
         <html>
         <body>
             <div>FOO</div>
         </body>
         </html>"""

    buffer = []
    parser = BaseParser(buffer, [FooTransform()])
    parser.feed(raw_html)
    assert ''.join(buffer) == output_html


def test_should_apply_multiple_transformers_to_html():
    raw_html = """
         <html>
         <body>
             <foo-content><p>Foo</p></foo-content>
             <bar-content><header>Hello World</header></bar-content>
             <leave-me-alone-content>I want to be alone</leave-me-alone-content>
         </body>
         </html>"""

    output_html = """
         <html>
         <body>
             <div>FOO</div>
             <h1>HELLO WORLD</h1>
             <leave-me-alone-content>I want to be alone</leave-me-alone-content>
         </body>
         </html>"""

    buffer = []
    parser = BaseParser(buffer, [FooTransform(), BarTransform()])
    parser.feed(raw_html)
    assert ''.join(buffer) == output_html
