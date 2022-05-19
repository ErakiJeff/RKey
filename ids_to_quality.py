import xml.etree.ElementTree as ET
import os


def get_item_ids_to_quality():
    path = os.path.join(os.path.dirname(__file__), "data/items_metadata.xml")
    with open(path, "r") as reader:
        item_ids_to_quality = {}
        tree = ET.parse(reader)
        items = tree.getroot()
        for item_element in items:
            if item_element.tag == "item":
                item_ids_to_quality[int(item_element.attrib["id"])] = int(
                    item_element.attrib["quality"]
                )
        return item_ids_to_quality
