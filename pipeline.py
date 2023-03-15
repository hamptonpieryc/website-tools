from os import walk

from hpyc_transformers import ContentPageTransformer
from html_transformer import Transformer, TransformingParser


class Pipeline:
    """ The pipeline that runs all tne the necessary HTML transforms and image manipulation"""

    def __init__(self, input_dir: str, output_dir: str, transformers: [Transformer] = [ContentPageTransformer()]):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.transformers = transformers

    def run(self):
        with open(self.input_dir + '/layout.html', "r") as f:
            layout = ''.join(f.readlines())
        print("layout.html is " + str(len(layout)) + " characters")

        files = []
        for (dirpath, dirnames, filenames) in walk(self.input_dir + '/content'):
            files.extend(filenames)
            break

        for i in files:
            with open(self.input_dir + '/content/' + i, "r") as f:
                raw = ''.join(f.readlines())

                # nested = NestedTransform(outer_tag='nested', transforms=[FooTransform(), BarTransform()])
                buffer = []
                parser = TransformingParser(buffer, self.transformers)
                parser.feed(raw)

                # transformer = Transformer(ContentPageTransformer())
                # transformed = transformer.transform(raw)

                with open(self.output_dir + "/" + i, "w") as saved:
                    processed = layout.replace("REPLACE-ME!", ''.join(buffer))
                    saved.write(processed)

        print("running the pipeline")
