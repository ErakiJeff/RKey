import config_reader
from game_data import get_player_starting_items
import re

# Capture group 1: item id
# Capture group 2: item name
# Capture group 3: player name
collectible_re = re.compile(r"Adding collectible (\d+) \(([^()]+)\).*\(([^()]+)\)")
starting_items = get_player_starting_items()


class IsaacLogParser:
    def __init__(self, log_file_location=None) -> None:
        if log_file_location != None:
            self.log_file_location = log_file_location
        else:
            self.log_file_location = config_reader.get_data("log_file_location")
        self.last_read_line = 0
        self.parse()

    def parse(self):
        with open(self.log_file_location, "r") as reader:
            lines = reader.readlines()
            self.new_lines = lines[self.last_read_line :]
            self.last_read_line = len(lines)

    def is_in_new_lines(self, search_term):
        for line in self.new_lines:
            if search_term in line:
                return True
        return False

    def get_line_in_new_lines(self, search_term):
        for line in reversed(self.new_lines):
            if search_term in line:
                return line
        return None

    def get_most_recent_item(self):
        item_line = self.get_line_in_new_lines("Adding collectible")
        match = None
        if item_line != None:
            match = collectible_re.search(item_line)
        if match != None:
            item_id = int(match[1])
            item_name = match[2]
            character_name = match[3]

            if item_id not in starting_items[character_name]:
                return (item_id, item_name, character_name)

    def flush_new_lines(self):
        self.new_lines = []
