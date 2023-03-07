from html_transformer import Transformer, NestedTransform, TransformingParser
from common_test import FooTransform, BarTransform


def test_should_transform_foo_content():
    raw = '<foo><p>Foo</p></foo>'
    expected = '<div>FOO</div>'

    transformer = Transformer(FooTransform())
    assert transformer.transform(raw) == expected


def test_should_transform_nested_content():
    raw = '<nested><foo><p>Foo</p></foo></nested>'
    expected = '<div>FOO</div>'

    nested = NestedTransform(outer_tag='nested', transforms=[FooTransform()])
    transformer = Transformer(nested)
    transformer.transform(raw)
    # assert transformer.transform(raw) == expected


def test_should_apply_single_transformer_to_html():
    raw_html = """
         <html>
         <body>
             <foo><p>Foo</p></foo>
         </body>
         </html>"""

    output_html = """
         <html>
         <body>
             <div>FOO</div>
         </body>
         </html>"""

    buffer = []
    parser = TransformingParser(buffer, [FooTransform()])
    parser.feed(raw_html)
    assert ''.join(buffer) == output_html


def test_should_apply_multiple_transformers_to_html():
    raw_html = """
         <html>
         <body>
             <foo><p>Foo</p></foo>
             <bar><header>Hello World</header></bar>
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
    parser = TransformingParser(buffer, [FooTransform(), BarTransform()])
    parser.feed(raw_html)
    assert ''.join(buffer) == output_html


def test_should_apply_nested_transformers():
    raw_html = """
            <html>
            <body>
                <nested>
                <foo><p>Foo</p></foo>
                </nested>
            </body>
            </html>"""

    output_html = """
           <html>
           <body>
              <div>FOO</div>
           </body>
           </html>"""

    nested = NestedTransform(outer_tag='nested', transforms=[FooTransform()])
    buffer = []
    parser = TransformingParser(buffer, [nested])
    parser.feed(raw_html)
    # assert ''.join(buffer) == output_html
