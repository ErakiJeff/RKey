import config_reader
from itertools import islice
import re

collectible_re = re.compile(r"Adding collectible (\d+) \(([^()]+)\)")


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
            self.new_lines = islice(lines, self.last_read_line, None)
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
        match = collectible_re.search(item_line)
        if match:
            item_id = int(match[1])
            item_name = match[2]
            return (item_id, item_name)
