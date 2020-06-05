import transmissionrpc
from transmissionrpc.torrent import Torrent
from common.utils import Utils
from typing import List
import models.games.game as Game


class Transmission:
    IP = '10.67.192.123'
    PORT = 9091
    tc = transmissionrpc.Client(IP, PORT)

    def __init__(self, magnet):
        self.magnet = magnet
        self.hashString = Utils.hash_from_magnet(
            magnet).lower() if magnet is not None else None

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

