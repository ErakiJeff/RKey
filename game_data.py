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


def get_player_starting_items():
    return {
        "Isaac": [105],
        "Magdalene": [45],
        "Cain": [46, 710],
        "Judas": [34, 705],
        "???": [36, 715],
        "Eve": [117, 126, 122, 713],
        "Samson": [157],
        "Azazel": [],
        "Lazarus": [214, 711],
        "Eden": [],
        "Lost": [609],
        "Lilith": [357, 412],
        "Keeper": [349],
        "Apollyon": [706, 477],
        "Forgotten": [],
        "Bethany": [712, 584],
        "Jacob": [722],
        "Esau": [],
    }
