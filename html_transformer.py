import xml.etree.ElementTree as ElementTree
from html_parser import BaseParser


class Transform:
    """A base class for running transforms. Override the transform method"""

    def __init__(self, outer_tag: str):
        self.outer_tag = outer_tag

    def transform(self, nodes: list) -> str:
        """Is passed the inner content nodes and should return the transformed content."""
        pass


class NestedTransform(Transform):
    """A transform that nests one or more inner transforms"""

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


class TransformingParser(BaseParser):
    """A parser that can apply one or more transforms
    """

    def __init__(self, content_buffer, transformers):
        BaseParser.__init__(self, content_buffer)
        self.transformers = transformers
        self.tag_names = list(map(lambda x: x.outer_tag, self.transformers))
        self.captured = []

    def handle_captured(self, tag_name, captured):
        fully_captured = "<" + tag_name + ">" + ''.join(captured) + "</" + tag_name + ">"
        filtered = list(filter(lambda t: t.outer_tag == tag_name, self.transformers))
        if len(filtered) == 1:
            transformer = Transformer(filtered[0])
            self.content_buffer.extend(transformer.transform(fully_captured))
        else:
            self.content_buffer.extend(fully_captured)


class CaptureElementsParser(BaseParser):
    """A html parser that scans for any elements that match the supplied tag_names and
       for each found the content is captured and added to the list of captured content
    """

    def __init__(self, tag_names):
        BaseParser.__init__(self, [])
        self.tag_names = tag_names
        self.captured = []

    def handle_captured(self, tag_name, captured):
        fully_captured = ''.join(captured)
        self.captured.append((tag_name, fully_captured))


class Transformer:
    def __init__(self, transform: Transform):
        self.__the_transform = transform

    def transform(self, raw):
        if isinstance(self.__the_transform, NestedTransform):
            tag_names = list(map(lambda x: x.outer_tag, self.__the_transform.transforms))
            capture = CaptureElementsParser(tag_names)
            capture.feed(raw)
            buffer = []
            for x in capture.captured:
                t = x[0]
                partial_html = '<root><' + t + '>' + x[1] + "</" + t + "></root>"
                tree = ElementTree.fromstring(partial_html)
                nodes = tree.find(".").find(t).findall("*")
                for t in self.__the_transform.transforms:
                    buffer.append(t.transform(nodes))
                    buffer.append("\n")

            return ''.join(buffer)

        else:
            tree = ElementTree.fromstring('<root>' + raw + "</root>")
            nodes = tree.find(".").find(self.__the_transform.outer_tag).findall("*")
            return self.__the_transform.transform(nodes)
