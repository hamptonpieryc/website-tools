from os import walk


class Pipeline:

    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run(self):
        layout = ''
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
                with open(self.output_dir + "/" + i, "w") as saved:
                    processed = layout.replace("REPLACE-ME!", raw)
                    saved.write(processed)

        print("running the pipeline")
