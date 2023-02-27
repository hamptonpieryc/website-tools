import xml.etree.ElementTree as ET

# raw = '<root><content><h1>Header</h1><p>Foo</p><p>Bar</p></content></root>'
#
# tree = ET.fromstring(raw)
#
# nodes = tree.find(".").find("content").findall("*")
# print(nodes)
#
#
# class ElementTransformer:
#     def __init__(self, matched_tag, transform):
#         self.matched_tag = matched_tag
#         self.transformer = transform
#
#     def matches(self, tag):
#         return tag == self.matched_tag
#
#     def transform(self, content):
#         return self.transformer(content)
#
#
# def foo_transformer(content):
#     return content + "opps"
#
#
# x = ElementTransformer("foo", foo_transformer)
# print(x.matches("foo"))
# print(x.transform("hello world"))


class Transform:
    def __init__(self, outer_tag: str):
        self.outer_tag = outer_tag

    def transform(self, nodes: list) -> str:
        """Is passed the inner content nodes and should return the transformed content."""
        pass


class Transformer:
    def __init__(self, transform: Transform):
        self.__the_transform = transform

    def transform(self, raw):
        tree = ET.fromstring('<root>' + raw + "</root>")
        nodes = tree.find(".").find(self.__the_transform.outer_tag).findall("*")
        return self.__the_transform.transform(nodes)
