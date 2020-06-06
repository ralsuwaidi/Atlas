# from models.game import Game
from models.games.game import Game
from pprint import pprint
from common.utils import Utils
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import re

Game.init_database()

for game in Game.all():
    if "&" in game.title:
        print(game.title)