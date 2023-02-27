import xml.etree.ElementTree as ElementTree


class Transform:
    """A base class for running transforms. Override the transform method"""

    def __init__(self, outer_tag: str):
        self.outer_tag = outer_tag

    def transform(self, nodes: list) -> str:
        """Is passed the inner content nodes and should return the transformed content."""
        pass


class Transformer:
    def __init__(self, transform: Transform):
        self.__the_transform = transform

    def transform(self, raw):
        tree = ElementTree.fromstring('<root>' + raw + "</root>")
        nodes = tree.find(".").find(self.__the_transform.outer_tag).findall("*")
        return self.__the_transform.transform(nodes)
