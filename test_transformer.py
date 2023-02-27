from transformer import Transform
from transformer import Transformer


def test_should_do_something():
    raw = '<content><p>Foo</p></content>'
    expected = '<div>Foo</div>'

    class FooTransform(Transform):
        def transform(self, nodes: list) -> str:
            result = ''
            for node in nodes:
                if node.tag == 'p':
                    result += '<div>' + str(node.text) + '</div>'
            return result

    transformer = Transformer(FooTransform('content'))
    assert transformer.transform(raw) == expected
