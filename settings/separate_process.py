import re
from copy import deepcopy as dc


class Dswedrftgyhuji(object):
    def __init__(self, pipe_connection, load_data, galactic_maps):
        self.pipe_connection = pipe_connection
        self.load_data = load_data
        self.galactic_maps = galactic_maps
        self._load_maps()
        self._send_package()

    def _send_package(self):
        self.pipe_connection.send([self.galactic_maps, self.load_data])

    def _operate(self, item, values):  # todo: jsony maja czasem strukture drzewkorza z kilkoma name trzeba to sprawdzic
        regrexf = re.compile(r'"name":"(?P<name>[^:",]*)",', re.I)
        regrex = re.compile(r'^.*"name":"(?P<name>[^:",]*)",', re.I)
        with open(values['path']) as maps:
            pass
            galactic_list = maps.readlines()
            values['systems'] = dc(len(galactic_list))
            [self.galactic_maps.add(regrexf.findall(x)[0]) for x in galactic_list if regrex.match(x)]
            print(f"POWERPLAY {values['systems']} SYSTEMS LOAED FROM {item}")
            del galactic_list
            maps.close()

    def _load_maps(self):  # dorobic obsluge koordynatow

        for item, values in self.load_data.items():
            if 'No' in values['loaded'] and 'Yes' in values['in_use']:
                self._operate(item, values)
                values['loaded'] = 'Yes'
