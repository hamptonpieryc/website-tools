import xml.etree.ElementTree as ElementTree


class Transform:
    """A base class for running transforms. Override the transform method"""

    def __init__(self, outer_tag: str):
        self.outer_tag = outer_tag

    def transform(self, nodes: list) -> str:
        """Is passed the inner content nodes and should return the transformed content."""
        pass


class NestedTransform(Transform):
    def __init__(self, outer_tag, transforms):
        self.outer_tag = outer_tag
        self.transforms = transforms

    def transform(self, nodes: list) -> str:
        result = ''
        for node in nodes:
            for transform in self.transforms:
                if transform.outer_tag == node.tag:
                    x = str(node)
                    transformer = Transformer(transform)
                    result += transformer.transform(node.text)

        return result


class Transformer:
    def __init__(self, transform: Transform):
        self.__the_transform = transform

    def transform(self, raw):
        if isinstance(self.__the_transform, NestedTransform):
            print("hhh")
            tag_names = list(map(lambda x: x.outer_tag, self.__the_transform.transforms))
            # capture = CaptureElementsParser(tag_names)
            # capture.feed(raw)
            # for x in capture.captured:
            #     print(x)

            return ""

        else:
            tree = ElementTree.fromstring('<root>' + raw + "</root>")
            nodes = tree.find(".").find(self.__the_transform.outer_tag).findall("*")
            return self.__the_transform.transform(nodes)
