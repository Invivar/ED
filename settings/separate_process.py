import json


class Dswedrftgyhuji(object):
    def __init__(self, pipe_connection):
        self.pipe_connection = pipe_connection
        self.galactic_maps = []
        self._load_maps()
        self._send_package()

    def _send_package(self):
        self.pipe_connection.send(self.galactic_maps)

    def _load_maps(self):
        with open(r'powerPlay.json') as maps:
            self.galactic_maps_list = json.load(maps)
            self.galactic_maps = [x['name'] for x in self.galactic_maps_list]
            del self.galactic_maps_list
            maps.close()
            print("POWERPLAY LOAED")
