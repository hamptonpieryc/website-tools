from textwrap import dedent
from hpyc_transformers import TopPanelTransformer
from hpyc_transformers import ContentPanelTransformer
from transformer import Transformer


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

    transformer = Transformer(TopPanelTransformer('hpyc-top-panel'))
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

    transformer = Transformer(ContentPanelTransformer('hpyc-content-panel'))
    transformed = transformer.transform(raw)
    assert transformed.strip() == expected
