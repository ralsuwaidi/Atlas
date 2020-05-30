import re
import uuid
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from common.database import Database
from common import utils
import datetime
from dataclasses import dataclass, field
import random
from models.games.scrape import Scrape
from models.games.rawg import Rawg
from models.model import Model


@dataclass()
class Game(Scrape,Model):
    collection: str = field(init=False, default="games")
    URL: str = field(init=False, default="https://fitgirl-repacks.site/")
    title: str
    original_size: str
    repack_size: str
    image: str
    url: str
    entry_date: datetime
    magnet: str = field(repr=False, default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    tags: List = field(default=None)
    rawg:Rawg = field(default=None)

    def __post_init__(self, rawg_api=False):
        self.rawg = Rawg.get_by_id(self._id)

    def json(self):
        return {
            "_id": self._id,
            "title": self.title,
            "tags": self.tags,
            "original_size": self.original_size,
            "repack_size": self.repack_size,
            "magnet": self.magnet,
            "image": self.image,
            "entry_date": self.entry_date,
            "url": self.url
        }

    @classmethod
    def push_to_mongo(cls, _id, data):
        Database.update(cls.collection, {"_id": _id}, data)

    @classmethod
    def search(cls, value: str):
        return [cls(**elem) for elem in Database.search(cls.collection, value)]


