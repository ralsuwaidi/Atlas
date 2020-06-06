# from models.game import Game
from models.games.game import Game
from pprint import pprint
from common.utils import Utils
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import re

Game.init_database()

game = Game.find_one_by("_id", "5d2310492c3a426587c95da542ca87f8")
game.title = "Halo: The Master Chief Collection"
game.save_to_mongo()