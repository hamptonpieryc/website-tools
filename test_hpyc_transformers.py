from textwrap import dedent
from hpyc_transformers import TopPanelTransformer, ContentPageTransformer, ContentPanelTransformer
from html_transformer import Transformer
import re


def normalise_white_space(raw: str):
    normalised = re.sub(r"\t+", " ", raw.strip(), flags=re.UNICODE)
    normalised = re.sub(r"\n+", " ", normalised, flags=re.UNICODE)
    normalised = re.sub(r"\s+", " ", normalised, flags=re.UNICODE)
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
            <p>a content panel with an image</p>
        </hpyc-content-panel>""")

    expected = dedent("""
        <div class="columns col-gapless hpyc-section">
            <div class="column col-9">
                <p>a content panel with an image</p>
            </div>
        </div>
      """).strip()

    transformer = Transformer(ContentPanelTransformer())
    transformed = transformer.transform(raw)
    assert transformed.strip() == expected


def test_combined_transform():
    raw = """
        <hpyc-content>
            <hpyc-top-panel>
                <h1>Example Page</h1>
            </hpyc-top-panel>
            <hpyc-content-panel>
                 <p>a content panel with an image</p>
            </hpyc-content-panel>
        </hpyc-content>
       """

    expected = """
        <div class="columns col-gapless hpyc-section">
        <div class="column col-12">
            <h1>Example Page</h1>
        </div>
    </div> 
    <div class="columns col-gapless hpyc-section">
        <div class="column col-9">
            <p>a content panel with an image</p>
        </div>
    </div>
      """

    transformer = Transformer(ContentPageTransformer())
    transformed = transformer.transform(raw)
    assert normalise_white_space(transformed) == normalise_white_space(expected)
