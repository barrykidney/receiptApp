import json
import os
import re
from datetime import datetime


class ReceiptParser:

    def __init__(self):
        self.outlets = []
        self.outlet = ""

    @staticmethod
    def read_json_file(filepath):
        json_file = open(filepath)
        json_data = json.load(json_file)
        json_file.close()
        return json_data

    def parse_text(self, text):
        self.outlets = self.read_json_file(os.getcwd() + "/data/outlets.json")["outlets"]
        self.outlet = self.identify_outlet(text, self.outlets)

        date_formats_json = self.read_json_file(os.getcwd() + "/data/date_formats.json")
        datestamp = self.identify_datestamp(text, date_formats_json[self.outlet])
        print("The outlet is " + self.outlet + " and the date is " + str(datestamp))

    @staticmethod
    def identify_outlet(txt, lst):
        identified = "unknown"
        for line in txt.splitlines():
            for o in lst:
                if o in line.lower():
                    identified = o
                    break
            if identified != "unknown":
                break
        return identified

    @staticmethod
    def identify_datestamp(txt, format_list):
        d = False
        for line in txt.splitlines():
            match = re.search(r"\d{" + str(format_list[0]["day"]) + "}" + format_list[0]["sep"] + "\d{"
                              + str(format_list[0]["mnt"]) + "}" + format_list[0]["sep"] + "\d{"
                              + str(format_list[0]["yr"]) + "}", line)
            if match and d:
                d = min([d, datetime.strptime(match.group(), '%d/%m/%y').date()])
            elif match and not d:
                d = datetime.strptime(match.group(), '%d/%m/%y').date()

        if not d and len(format_list) > 1:
            for f in range(1, len(format_list) - 1):
                # TODO: cycle through other possible date identifiers
                print("trying other possible date identifiers")

        return d
