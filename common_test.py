# reusable test code
from html_transformer import Transform
from html_transformer import Transformer


class FooTransform(Transform):

    def __init__(self):
        Transform.__init__(self=self, outer_tag="foo")

    def transform(self, nodes: list) -> str:
        result = ''
        for node in nodes:
            if node.tag == 'p':
                result += '<div>' + str(node.text).upper() + '</div>'
        return result


class BarTransform(Transform):

    def __init__(self):
        self.outer_tag = "bar"

    def transform(self, nodes: list) -> str:
        result = ''
        for node in nodes:
            if node.tag == 'header':
                result += '<h1>' + str(node.text).upper() + '</h1>'
        return result

