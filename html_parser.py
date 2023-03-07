from html.parser import HTMLParser


class BaseParser(HTMLParser):
    """A base html parser that can look for specified tag(s).
    Normally a class should just override handle_captured method
    """

    def __init__(self, content_buf, tag_names=[]):
        HTMLParser.__init__(self=self, convert_charrefs=False)
        self.capture_mode = False
        self.current_tag = ''
        self.tag_names = tag_names
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
        else:
            self.content_buffer.append("</" + tag + ">")

    def handle_data(self, data):
        self.__pick_buffer().append(data)

    def handle_charref(self, name):
        self.__pick_buffer().append('&#' + name + ';')

    def handle_entityref(self, name):
        self.__pick_buffer().append('&' + name + ';')

    def handle_captured(self, tag_name, captured):
        fully_captured = "<" + tag_name + ">" + ''.join(captured) + "</" + tag_name + ">"
        print(fully_captured)
        self.content_buffer.extend(fully_captured)
