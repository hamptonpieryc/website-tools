from html_transformer import Transformer
from common_test import FooTransform


def test_should_transform_foo_content():
    raw = '<foo><p>Foo</p></foo>'
    expected = '<div>FOO</div>'

    transformer = Transformer(FooTransform())
    assert transformer.transform(raw) == expected
