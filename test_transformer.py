from transformer import Transform
from transformer import Transformer


def test_transform_content():
    raw = '<content><p>Foo</p></content>'
    expected = '<div>FOO</div>ggg'

    class FooTransform(Transform):
        def transform(self, nodes: list) -> str:
            result = ''
            for node in nodes:
                if node.tag == 'p':
                    result += '<div>' + str(node.text).upper() + '</div>'
            return result

    transformer = Transformer(FooTransform('content'))
    assert transformer.transform(raw) == expected
