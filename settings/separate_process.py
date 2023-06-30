import json
from copy import deepcopy as dc


class Dswedrftgyhuji(object):
    def __init__(self, pipe_connection, load_data):
        self.pipe_connection = pipe_connection
        self.load_data = load_data
        self.galactic_maps = []
        self._load_maps()
        self._send_package()

    def _send_package(self):
        self.pipe_connection.send([self.galactic_maps, self.load_data])

    def _operate(self, item, values):
        with open(values['path']) as maps:
            pass
            self.galactic_list = json.load(maps)
            values['systems'] = dc(len(self.galactic_list))
            [self.galactic_maps.append(x['name']) for x in self.galactic_list if x['name'] not in self.galactic_maps]
            print(f"POWERPLAY {values['systems']} SYSTEMS LOAED FROM {item}")
            del self.galactic_list
            maps.close()

    def _load_maps(self):  # dorobic obsluge koordynatow

        for item, values in self.load_data.items():
            if 'No' in values['loaded'] and 'Yes' in values['in_use']:
                self._operate(item, values)
                values['loaded'] = 'Yes'
