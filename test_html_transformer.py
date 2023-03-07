from html_transformer import Transformer, NestedTransform
from common_test import FooTransform


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
    #assert transformer.transform(raw) == expected
