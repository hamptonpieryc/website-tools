from html_transformer import Transform
from html_transformer import NestedTransform
import random
import string


class IdGenerator:
    def next_id(self):
        return ''.join(random.sample(string.ascii_lowercase, 6))


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

    def __init__(self, id_gen: IdGenerator = IdGenerator()):
        Transform.__init__(self, 'hpyc-content-panel')
        self.id_gen = id_gen

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

        if len(paras) == 1:
            result += '\t\t<p>' + paras[0] + '\n\t\t</p>\n'
        elif len(paras) > 1:
            button_id = self.id_gen.next_id()
            more_content_id = self.id_gen.next_id()
            result += '\t\t<p>' + paras.pop(0)
            result += '\n\t\t\t<button class="hpyc-more" id="' + button_id \
                      + '" onclick="expand(\'' + button_id + '\',\'' + more_content_id + '\')"></button>\n'
            result += '\t\t</p>\n'
            result += '\t\t<div id="' + more_content_id + '" style="display: none;">\n'
            # paras.pop(0)

            for para in paras:
                result += '\t\t\t<p>' + para
                if para == paras[-1]:
                    result += '\n\t\t\t\t<button class="hpyc-less" onclick="collapse(\'' \
                              + button_id + '\',\'' + more_content_id + '\')"></button>'

                result += '\n\t\t\t</p>\n'

            result += '\t\t</div>\n'

        # class ="hpyc-more" id="bt2" onclick="expand('bt2','ct2')" > < / button >
        #
        # result += '\t\t<p>' + paras[0] + '</p>\n'
        #
        # if len(paras > 1):
        #     for para in paras.pop(0):
        #         result += '\t\t<p>' + para + '\n'
        #         if first_para and len(paras) > 1:
        #             result += '\t\t\t<button class="hpyc-more" id="bt2" onclick="expand(\'bt2\',\'ct2\')"></button>\n'
        #     result += '\t\t</p>\n'
        #     first_para = False

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
