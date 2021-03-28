import transmissionrpc
from transmissionrpc.torrent import Torrent
from common.utils import Utils
from typing import List
import models.games.game as Game


class Transmission:
    IP = '127.0.0.1'
    PORT = 9091
    tc = transmissionrpc.Client(IP, PORT)

    def __init__(self, magnet):
        self.magnet = magnet
        # print(magnet)
        try:
            self.hashString = Utils.hash_from_magnet(
                magnet).lower() 
        except:
            self.hashString = None
            
    def remove_torrent(self):
        Transmission.tc.remove_torrent(self.hashString)

    @classmethod
    def all(cls) -> Torrent:
        return cls.tc.get_torrents()

    def download(self):
        Transmission.tc.add_torrent(self.magnet)

    @classmethod
    def download_from_id(cls, _id):
        magnet = Game.Game.get_by_id(_id).magnet
        cls.tc.add_torrent(magnet)

