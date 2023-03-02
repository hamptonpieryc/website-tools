from html.parser import HTMLParser
from os import walk

# constants for HTML elements
TOP_PANEL = 'hpyc-top-panel'
CONTENT_PANEL = 'hpyc-content-panel'
HPYC_CONTENT = 'hpyc-content'


#
# A base html parser that can look for specified tag(s)
# Normally a class should just override handle_captured method
#
class BaseParser(HTMLParser):
    def __init__(self, tag_names, content_buf):
        HTMLParser.__init__(self=self, convert_charrefs=False)
        self.capture_mode = False
        self.tag_names = tag_names
        self.current_tag = ''
        self.capture_buffer = []
        self.content_buffer = content_buf

    def __pick_buffer(self):
        if self.capture_mode:
            return self.capture_buffer
        else:
            return self.content_buffer

    def handle_starttag(self, tag, attrs):
        # trigger when one of our expected tags is found
        # and go into capture mode.
        if tag in self.tag_names and not self.capture_mode:
            self.capture_mode = True
            self.current_tag = tag
            return

        if self.capture_mode and not tag == self.current_tag:
            buffer_to_use = self.capture_buffer
        else:
            buffer_to_use = self.content_buffer

        buffer_to_use.append("<" + tag)
        for attr in attrs:
            buffer_to_use.append(' ' + attr[0] + '=')
            buffer_to_use.append('"' + attr[1] + '"')
        buffer_to_use.append(">")

    def handle_endtag(self, tag):
        if self.capture_mode:
            if not tag == self.current_tag:
                self.capture_buffer.append("</" + tag + ">")
            else:
                self.capture_mode = False
                self.handle_captured(self.current_tag, self.capture_buffer)
                self.current_tag = ''
                self.capture_buffer = []

    def handle_data(self, data):
        self.__pick_buffer().append(data)

    def handle_charref(self, name):
        self.__pick_buffer().append('&' + name + ';')

    def handle_entityref(self, name):
        self.__pick_buffer().append('&' + name + ';')

    def handle_captured(self, tag_name, captured):
        self.content_buffer.extend(captured)


#
# A base html parser that can look for specified tag(s)
# Normally a class should just override handle_captured method
#
class ContentTransformer(HTMLParser):
    def __init__(self, paths, content_buf):
        HTMLParser.__init__(self=self, convert_charrefs=False)
        self.capture_mode = False
        self.paths = paths
        self.current_tag = ''
        self.capture_buffer = []
        self.content_buffer = content_buf

    def __pick_buffer(self):
        if self.capture_mode:
            return self.capture_buffer
        else:
            return self.content_buffer

    def handle_starttag(self, tag, attrs):
        # trigger when one of our expected tags is found
        # and go into capture mode.
        if tag in self.paths and not self.capture_mode:
            self.capture_mode = True
            self.current_tag = tag
            return

        if self.capture_mode and not tag == self.current_tag:
            buffer_to_use = self.capture_buffer
        else:
            buffer_to_use = self.content_buffer

        buffer_to_use.append("<" + tag)
        for attr in attrs:
            buffer_to_use.append(' ' + attr[0] + '=')
            buffer_to_use.append('"' + attr[1] + '"')
        buffer_to_use.append(">")

    def handle_endtag(self, tag):
        if self.capture_mode:
            if not tag == self.current_tag:
                self.capture_buffer.append("</" + tag + ">")
            else:
                self.capture_mode = False
                self.handle_captured(self.current_tag, self.capture_buffer)
                self.current_tag = ''
                self.capture_buffer = []

    def handle_data(self, data):
        self.__pick_buffer().append(data)

    def handle_charref(self, name):
        self.__pick_buffer().append('&' + name + ';')

    def handle_entityref(self, name):
        self.__pick_buffer().append('&' + name + ';')

    def handle_captured(self, tag_name, captured):
        self.content_buffer.extend( (tag_name, ''.join(captured)))


class LayoutParser(HTMLParser):

    def __init__(self, hpyc_content):
        HTMLParser.__init__(self)
        self.hpyc_content = hpyc_content
        self.hpyc_tag = False
        self.combined = []

    def handle_starttag(self, tag, attrs):
        if tag == HPYC_CONTENT:
            self.hpyc_tag = True
        else:
            self.combined.append("<" + tag)
            for attr in attrs:
                self.combined.append(' ' + attr[0] + '=')
                self.combined.append('"' + attr[1] + '"')
            self.combined.append(">")

    def handle_endtag(self, tag):
        if tag == HPYC_CONTENT and self.hpyc_tag:
            self.hpyc_tag = False
            self.combined.append(self.hpyc_content)
        else:
            self.combined.append("</" + tag + ">")

    def handle_data(self, data):
        if not self.hpyc_tag:
            self.combined.append(data)

    def processed(self):
        return ''.join(self.combined)


# process a <hpyc-top-panel> tag
class TopPanelParser(BaseParser):
    def __init__(self, content_buffer):
        BaseParser.__init__(self, TOP_PANEL, content_buffer)

    def handle_captured(self, tag_name, captured):
        self.content_buffer.extend("boo")
        print("in handle_captured for TopPanelParser ")


class PanelParser(BaseParser):
    def __init__(self, content_buffer):
        BaseParser.__init__(self, [TOP_PANEL, CONTENT_PANEL], content_buffer)

    def handle_captured(self, tag_name, captured):
        if tag_name == TOP_PANEL:
            parser = TopPanelParser(content_buffer)
            parser.feed(''.join(captured))
            # super().handle_captured(tag_name, captured)
        elif tag_name == CONTENT_PANEL:
            super().handle_captured(tag_name, captured)
        else:
            super().handle_captured(tag_name, captured)


# process a <hpyc-content> tag
class ContentParser(BaseParser):
    def __init__(self, content_buffer):
        BaseParser.__init__(self, HPYC_CONTENT, content_buffer)

    def handle_captured(self, tag_name, captured):
        print('processing tag:' + tag_name + '-' + ''.join(captured))
        panel_parser = PanelParser(content_buffer)
        panel_parser.feed(''.join(captured))
        # super().handle_captured(tag_name, captured)


# read the layout file
layout = ''
with open("templates/layout.html", "r") as f:
    layout = ''.join(f.readlines())
print("layout.html is " + str(len(layout)) + " characters")

files = []
for (dirpath, dirnames, filenames) in walk("content"):
    files.extend(filenames)
    break

for i in files:
    with open("content/" + i, "r") as f:
        content_buffer = []
        content_parser = ContentParser(content_buffer)
        content_parser.feed(''.join(f.readlines()))
        processed = ''.join(content_buffer)
        print("Processing content file:" + i + ", with " + str(len(processed)) + " characters")
        layout_parser = LayoutParser(processed)
        layout_parser.feed(layout)
        with open(i, "w") as saved:
            saved.write(layout_parser.processed())
