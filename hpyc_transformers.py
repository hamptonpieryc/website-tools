from html_transformer import Transform
from html_transformer import NestedTransform


class TopPanelTransformer(Transform):

    def __init__(self):
        Transform.__init__(self, 'hpyc-top-panel')

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
    """
      <div class="columns col-gapless hpyc-section">
        <div class="column col-3 ">
            <span class="hpyc-image">
            <img class="img-responsive" src="images/looking-to-join/kayak.jpeg">
                </span>
        </div>
        <div class="column col-9">
            <br>
            <h2>Kayaks and Canoes</h2>
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
                et dolore magna aliqua.
                <button class="hpyc-more" id="bt2" onclick="expand('bt2','ct2')"></button>
            </p>
            <div id="ct2" style="display: none;">
                <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
                    et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
                    aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
                    cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
                    culpa qui officia deserunt mollit anim id est laborum.
                    <button class="hpyc-less" onclick="collapse('bt2','ct2')"></button>
                </p>
            </div>

            <span class="hpyc-link-bar">
                <a href="join">Join</a>
                <a href="kayaker">Kayaking Group</a>
                <a href="kayak-storage">Kayak Storage</a>
            </span>
        </div>
    </div>
    """

    def __init__(self):
        Transform.__init__(self, 'hpyc-content-panel')

    def transform(self, nodes: list) -> str:
        header = '???'
        paras = []
        image = {}

        #  capture the date needed from the DOM
        for node in nodes:
            if node.tag == 'p':
                paras.append(str(node.text))
            elif node.tag == 'header':
                header = str(node.text)
            elif node.tag == 'img':
                image["href"] = node.attrib["href"]

        # Build the HTML snippet
        result = '\n'
        result += '<div class="columns col-gapless hpyc-section\">\n'

        # Image
        result += '\t<div class="column col-3">\n'
        result += '\t\t<span class="hpyc-image">\n'
        result += '\t\t\t<img class="img-responsive" src="' + image.get("href", "placeholder.jpg") + '">\n'
        result += '\t\t</span>\n'
        result += '\t</div>\n'

        # Content
        result += '\t<div class=\"column col-9\">\n'
        result += '\t\t<h2>' + header + '</h2>\n'


        """
          <div class="column col-3 ">
            <span class="hpyc-image">
            <img class="img-responsive" src="images/looking-to-join/kayak.jpeg">
                </span>
        </div>
        """

        # result += '\t\t' + '<p>' + str(node.text) + '</p>\n'

        result += "\t" + '</div>\n'
        result += '</div>\n'
        return result.replace("\t", "    ")  # 4 spaces per tab for consistent formatting


class ContentPageTransformer(NestedTransform):

    def __init__(self):
        NestedTransform.__init__(self, 'hpyc-content', [TopPanelTransformer(), ContentPanelTransformer()])
