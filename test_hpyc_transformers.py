from textwrap import dedent
from hpyc_transformers import TopPanelTransformer
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
    """)

    transformer = Transformer(TopPanelTransformer('hpyc-top-panel'))
    transformed = transformer.transform(raw)
    assert transformed == expected
