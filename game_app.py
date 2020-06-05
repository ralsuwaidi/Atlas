# from models.game import Game
from models.games.game import Game
from pprint import pprint
from common.utils import Utils

Game.init_database()

for game in Game.random(3):
    print(game.magnet)
    print(game.torrent.hashString)
    game.torrent.download()