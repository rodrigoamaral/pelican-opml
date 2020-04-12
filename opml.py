import sys
from lxml import etree


def _is_valid_opml(root):
    return len(root) > 1 and root[0].tag == "head" and root[1].tag == "body"


def _is_leaf_node(e):
    return len(e) == 0


class InvalidOPMLException(Exception):
    pass


class OPML:
    def __init__(self, filename):
        self._tree = self._parse_opml(filename)
        self._root = self._tree.getroot()

        if not _is_valid_opml(self._root):
            raise InvalidOPMLException(f"{filename} is an invalid OPML file!")

        self.outlines = [e for e in self._root.iter("outline") if _is_leaf_node(e)]


    def _parse_opml(self, filename):
        with open(filename, "r") as f:
            return etree.parse(f)


    def to_markdown(self):
        return "\n".join(f"- [{item.get('text')}]({item.get('xmlUrl')})" for item in self.outlines)


    def to_html(self):
        pass




if __name__ == "__main__":
    
    if len(sys.argv) <= 1:
        raise SystemExit(1)
    
    input_file = sys.argv[1]

    opml = OPML(input_file)
    print(opml.to_markdown())
