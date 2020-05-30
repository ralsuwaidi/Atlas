# from models.game import Game
from common.database import Database
import datetime
from models.games.game import Game
from difflib import SequenceMatcher
from models.games.rawg import Rawg

# game = Game.random()[0]
# print(game.title)
# print(game.rawg.title)
# print(game.json())


game = Game.random()[0]
print(game._id)
print(game.rawg._id)