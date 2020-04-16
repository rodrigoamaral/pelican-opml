import sys
import os
from lxml import etree
from pelican import signals

from .opml import OPML


OPML_PATH = os.path.join("content", "opml")


def init_opml(generator):
    generator.context["opml_data"] = {}


def add_opml(generator, metadata):
    if "opml" in metadata.keys():
        opml_data = OPML(os.path.join(OPML_PATH, metadata["opml"]))
        generator.context["opml_data"]["to_html"] = opml_data.to_html()


def register():
    signals.page_generator_init.connect(init_opml)
    signals.page_generator_context.connect(add_opml)