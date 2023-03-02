from transformer import Transform


class TopPanelTransformer(Transform):
    def transform(self, nodes: list) -> str:
        result = '<div class="columns col-gapless hpyc-section\">\n'
        result += '\t<div class=\"column col-12\">\n'

        for node in nodes:
            if node.tag == 'h1':
                result += '\t\t' + '<h1>' + str(node.text) + '</h1>\n'
            elif node.tag == 'p':
                result += '\t\t' + '<p>' + str(node.text) + '</p>\n'

        result += "\t" + '</div>\n'
        result += '</div>\n'
        return result.replace("\t", "    ")  # 4 spaces per tab for consistent formatting


class ContentPanelTransformer(Transform):
    def transform(self, nodes: list) -> str:
        result = '\n'
        result += '<div class="columns col-gapless hpyc-section\">\n'
        result += '\t<div class=\"column col-9\">\n'

        for node in nodes:
            if node.tag == 'p':
                result += '\t\t' + '<p>' + str(node.text) + '</p>\n'

        result += "\t" + '</div>\n'
        result += '</div>\n'
        return result.replace("\t", "    ")  # 4 spaces per tab for consistent formatting
