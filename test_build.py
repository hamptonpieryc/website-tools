# def inc(x):
#     return x + 1
#
#
# def test_answer():
#     assert inc(3) == 4

from build import ContentParser
from build import TopPanelParser

# minimal top panel
top_panel_html = '''
<hpyc-top-panel>
       <h1>Example Page</h1>
       <p>Lorem Ipsum</p>
</hpyc-top-panel>
'''

# top panel converted to full html
processed = '''
<h1 class="header">Example Page</h1>
<div>Lorem Ipsum</p>
'''


def test_parser():
    content_buffer = []
    content_parser = TopPanelParser(content_buffer)
    content_parser.feed(top_panel_html)
    processed = ''.join(content_buffer)
    print(processed)
    assert processed == "\nboo\n"

