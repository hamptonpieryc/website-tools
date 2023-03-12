from os import makedirs

from textwrap import dedent
import random
import string

from pipeline import Pipeline


def random_token():
    return ''.join(random.sample(string.ascii_lowercase, 6))


def create_test_directories():
    token = random_token()
    input_dir = ".testing/" + token + "/raw"
    output_dir = ".testing/" + token + "/processed"
    makedirs(input_dir)
    makedirs(input_dir + "/content")
    makedirs(output_dir)
    return input_dir, output_dir


def read_text_file(filename: str) -> str:
    content = ''
    with open(filename, "r") as f:
        content = ''.join(f.readlines())
    return content


def create_text_file(filename: str, content: str):
    with open(filename, 'w') as f:
        f.write(content)


def test_should_apply_layout_to_file():
    layout = dedent("""
            <html>
            <body>
                <div>REPLACE-ME!</div>
            </body>
            </html>
    """).strip()

    page1 = dedent("""
            <p>Hello World</p>
    """).strip()

    expected = dedent("""
                <html>
                <body>
                    <div><p>Hello World</p></div>
                </body>
                </html>
        """).strip()

    # create test data
    test_dirs = create_test_directories()
    create_text_file(test_dirs[0] + '/layout.html', layout)
    create_text_file(test_dirs[0] + '/content/page1.html', page1)

    pipeline = Pipeline(test_dirs[0], test_dirs[1])
    pipeline.run()

    processed = read_text_file(test_dirs[1] + '/page1.html')
    print(processed)

    assert processed == expected