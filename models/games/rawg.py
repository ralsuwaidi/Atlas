import datetime
import pprint
import uuid
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import List, Dict

import requests

from models.model import Model


@dataclass
class Rawg(Model):
    collection: str = field(init=False, default="rawg")
    title: str = field(default=None)
    image: str = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    release_date: datetime = field(default=None)
    r_exceptional: float = field(default=None)
    r_meh: float = field(default=None)
    r_recommended: float = field(default=None)
    r_skip: float = field(default=None)
    screenshots: List[str] = field(default_factory=list)

    @staticmethod
    def match_ratio(game_title, rawg_title, ratio_limit: float = 0.8) -> bool:
        ratio = SequenceMatcher(None, game_title.lower(),
                                rawg_title.lower()).ratio()
        if game_title.lower() in rawg_title.lower() or rawg_title.lower() in game_title.lower() or ratio > ratio_limit:
            return True
        else:
            return False

    def api(self, game_title: str = None)-> "Rawg":
        parameters = {
            "search": game_title or self.title,
            "page_size": 1
        }
        response = requests.get("https://rawg.io/api/games", params=parameters)

        response_json = response.json()["results"][0]

        # pprint.pprint(response_json)
        self.title = response_json["name"]

        self.image = response_json["background_image"]
        try:
            self.release_date = datetime.datetime.strptime(
                response_json["released"], "%Y-%m-%d")
        except:
            pass

        self.screenshots = []
        try:
            for screenshot in response_json['short_screenshots']:
                self.screenshots.append(screenshot['image'])
        except:
            pass
        # print(response_json['short_screenshots'][0]['image'])

        # ratings from rawg
        self.r_recommended = "null"
        self.r_exceptional = "null"
        self.r_meh = "null"
        self.r_skip = "null"

        # if we have a rating
        if len(response_json["ratings"]) > 0:
            for rating in response_json["ratings"]:
                if rating["title"] == "recommended":
                    self.r_recommended = rating["percent"]
                if rating["title"] == "meh":
                    self.r_meh = rating["percent"]
                if rating["title"] == "exceptional":
                    self.r_exceptional = rating["percent"]
                if rating["title"] == "skip":
                    self.r_skip = rating["percent"]

        return self

    def get_score(self) -> int:
        score_p = 0
        score_n = 0

        if isinstance(self.r_exceptional, float):
            score_p+=self.r_exceptional
        if isinstance(self.r_recommended, float):
            score_p+=self.r_recommended
        
        if isinstance(self.r_meh, float):
            score_n+=self.r_meh
        if isinstance(self.r_skip, float):
            score_n+=self.r_skip


        total = score_n+score_p
        if total==0:
            return None
        return int((score_p/total)*100)


    def json(self):
        return {
            "_id": self._id,
            "image": self.image,
            "title": self.title,
            "release_date": self.release_date,
            "r_exceptional": self.r_exceptional,
            "r_meh": self.r_meh,
            "r_recommended": self.r_recommended,
            "r_skip": self.r_skip,
            "screenshots": self.screenshots
        }

    def website(self):
        return f"https://rawg.io/games/{self.api()['slug']}"
