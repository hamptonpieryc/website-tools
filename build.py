from html.parser import HTMLParser
from os import walk

from textwrap import dedent
from hpyc_transformers import TopPanelTransformer, ContentPageTransformer, ContentPanelTransformer, IdGenerator
from html_transformer import Transformer
import re


# constants for HTML elements
TOP_PANEL = 'hpyc-top-panel'
CONTENT_PANEL = 'hpyc-content-panel'
HPYC_CONTENT = 'hpyc-content'


# read the layout file
layout = ''
with open("templates/layout.html", "r") as f:
    layout = ''.join(f.readlines())
print("layout.html is " + str(len(layout)) + " characters")

files = []
for (dirpath, dirnames, filenames) in walk("test_content"):
    files.extend(filenames)
    break

for i in files:
    with open("content/" + i, "r") as f:
        content_buffer = []
        transformer = Transformer(ContentPageTransformer())
        #     transformed = transformer.transform(raw)

        raw = ''.join(f.readlines())
        transformed = transformer.transform(raw)

        processed = ''.join(content_buffer)
        print("Processing content file:" + i + ", with " + str(len(processed)) + " characters")
        #layout_parser = LayoutParser(processed)
        #layout_parser.feed(layout)
        #with open(i, "w") as saved:
        #    saved.write(layout_parser.processed())
