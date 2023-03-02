from build import ContentTransformer


def test_foo():
    def shout(text):
        return text.upper()

    def whisper(text):
        return text.lower()

    def greet(func):
        # storing the function in a variable
        greeting = func("Hi, I am created by a function passed as an argument.")
        print(greeting)

    greet(shout)
    greet(whisper)


def test_should_transform_single_matching_tag():
    raw = '<content><p>Foo</p></content>'
    expected = '<div>Foo<div>'

    thistuple = ("apple", "banana", "cherry")
    print(thistuple)

    def transform(tags):
        print(tags)

    transformed = ContentTransformer(['content/p'], transform).feed(raw)
    print(transformed)
