from textwrap import dedent
from hpyc_transformers import TopPanelTransformer, ContentPanelTransformer, IdGenerator
from html_transformer import Transformer
import re


class FixedIdGenerator(IdGenerator):
    """Make it easy to control the ids generated within the transformed HTML"""

    def __init__(self):
        self.index = -1
        self.ids = ["id1", "id2", "id3", "id4", "id5"]

    def next_id(self):
        self.index += 1
        return self.ids[self.index]


def normalise_white_space(raw: str):
    normalised = re.sub(r"\s+", " ", raw.strip(), flags=re.UNICODE)
    return normalised


def test_normalise():
    assert normalise_white_space(" foo  bar") == "foo bar"
    assert normalise_white_space(" foo \t bar") == "foo bar"
    assert normalise_white_space(" foo \nbar ") == "foo bar"


def test_top_panel_transform():
    raw = dedent("""
        <hpyc-top-panel>
            <h1>Example Page</h1>
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
        </hpyc-top-panel>
    """)

    expected = dedent("""
        <div class="columns col-gapless hpyc-section">
            <div class="column col-12">
                <h1>Example Page</h1>
                <p>Paragraph 1</p>
                <p>Paragraph 2</p>
            </div>
        </div>
    """).strip()

    transformer = Transformer(TopPanelTransformer())
    transformed = transformer.transform(raw)
    assert transformed.strip() == expected


def test_content_panel_transform():
    raw = dedent("""
        <hpyc-content-panel>
            <header>Example</header>
            <p>Paragraph 1</p>
            <p>Paragraph Two</p>
            <p>Last Paragraph</p>
            <img href=\"image.jpg\"></img>
        </hpyc-content-panel>""")

    expected = dedent("""
        <div class="columns col-gapless hpyc-section">
            <div class="column col-3">
                <span class="hpyc-image">
                    <img class="img-responsive" src="image.jpg">
                </span>
            </div>
            <div class="column col-9">
                <h2>Example</h2>
                <p>Paragraph 1
                    <button class="hpyc-more" id="id1" onclick="expand('id1','id2')"></button>
                </p>
                <div id="id2" style="display: none;">
                    <p>Paragraph Two
                    </p>
                    <p>Last Paragraph
                        <button class="hpyc-less" onclick="collapse('id1','id2')"></button>
                    </p>
                </div>
            </div>
        </div>
      """).strip()

    transformer = Transformer(ContentPanelTransformer(FixedIdGenerator()))
    transformed = transformer.transform(raw)
    assert transformed.strip() == expected

# todo - this test is too hard to maintain
# maybe just check snippets
# def test_combined_transform():
#     raw = """
#         <hpyc-content>
#             <hpyc-top-panel>
#                 <h1>Example Page</h1>
#             </hpyc-top-panel>
#             <hpyc-content-panel>
#                  <p>a content panel with an image</p>
#             </hpyc-content-panel>
#         </hpyc-content>
#        """
#
#     expected = """
#         <div class="columns col-gapless hpyc-section">
#         <div class="column col-12">
#             <h1>Example Page</h1>
#         </div>
#     </div>
#     <div class="columns col-gapless hpyc-section">
#         <div class="column col-9">
#             <p>a content panel with an image</p>
#         </div>
#     </div>
#       """
#
#     transformer = Transformer(ContentPageTransformer())
#     transformed = transformer.transform(raw)
#     assert normalise_white_space(transformed) == normalise_white_space(expected)
