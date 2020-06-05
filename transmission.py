from models.transmission import Transmission

for torrent in Transmission.all():
    torrent.remove_torrent()