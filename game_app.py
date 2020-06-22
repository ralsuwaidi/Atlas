# from models.game import Game
from models.games.game import Game
from pprint import pprint
from common.utils import Utils
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import re

Game.init_database()

print(Game.find_one_by("title", "Far Cry: New Dawn – Deluxe Edition"))