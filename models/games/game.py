import re
import uuid
from typing import List

from common.database import Database
import datetime
from dataclasses import dataclass, field
from models.games.scrape import Scrape
from models.games.rawg import Rawg
from models.model import Model
from models.transmission import Transmission


@dataclass()
class Game(Scrape, Model):
    collection: str = field(init=False, default="games")
    URL: str = field(init=False, default="https://fitgirl-repacks.site/")
    title: str
    original_size: str
    repack_size: str
    image: str
    url: str
    entry_date: datetime
    description: str = field(default=None)
    magnet: str = field(repr=False, default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    tags: List = field(default=None)
    rawg: Rawg = field(default=None)

    def __post_init__(self, rawg_api=False):
        self.rawg = Rawg.get_by_id(self._id)
        self.torrent = Transmission(self.magnet)

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
            "url": self.url,
            "description": self.description
        }

    @classmethod
    def push_to_mongo(cls, _id, data):
        Database.update(cls.collection, {"_id": _id}, data)

    @classmethod
    def search(cls, value: str):
        return [cls(**elem) for elem in Database.search(cls.collection, value)]

