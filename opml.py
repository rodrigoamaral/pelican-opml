import sys
import json
from lxml import etree


class InvalidOPMLException(Exception):
    pass


class OPML:
    """Represents a basic OPML structure for a list of feed links.
    
    """
    def __init__(self, filename):
        self._sourcefile = filename
        self._tree = self._parse_opml()
        self._root = self._get_root()
        self.outlines = sorted([e for e in self._root.iter("outline") if self._is_leaf_node(e)], key=lambda item: item.get("text"))


    def __len__(self):
        return len(self.outlines)


    def __iter__(self):
        return iter(self.outlines)


    def _parse_opml(self):
        with open(self._sourcefile, "r") as f:
            return etree.parse(f)


    def _get_root(self):
        root = self._tree.getroot()
        
        if not self._is_valid_opml(root):
            raise InvalidOPMLException(f"{self._sourcefile} is an invalid OPML file!")

        return root


    def _is_valid_opml(self, root):
        return len(root) > 1 and root[0].tag == "head" and root[1].tag == "body"


    def _is_leaf_node(self, e):
        return len(e) == 0


    def to_markdown(self):
        """Retrieve links as a mardown list string."""

        return "\n".join(f"- [{item.get('text')}]({item.get('xmlUrl')})" for item in self.outlines)


    def to_html(self):
        """Retrieve links as a HTML list string."""

        list_items = "\n".join(f"\t<li><a href=\"{item.get('xmlUrl')}\">{item.get('text')}</a></li>" for item in self.outlines)

        return f"<ul>\n{list_items}\n</ul>"


    def to_json(self, ensure_ascii=False):
        """Retrieve links as a JSON object list string."""

        json_items = [{'text': item.get('text'), 'xmlUrl': item.get('xmlUrl')} for item in self.outlines]

        return json.dumps(json_items, ensure_ascii=ensure_ascii)


if __name__ == "__main__":
    
    if len(sys.argv) <= 1:
        raise SystemExit(1)
    
    input_file = sys.argv[1]

    opml = OPML(input_file)
    print(opml.to_markdown())
    print(opml.to_html())
    print(opml.to_json())
