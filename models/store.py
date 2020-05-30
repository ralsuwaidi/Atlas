import uuid
from typing import Dict
from models.model import Model
import re
from dataclasses import dataclass, field

@dataclass(eq=False)
class Store(Model):
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    collection: str = field(init=False, default="stores")

    def json(self) -> Dict:
        return {
            "_id":self._id,
            "name":self.name,
            "url_prefix":self.url_prefix,
            "tag_name":self.tag_name,
            "query":self.query
        }

    @classmethod
    def get_by_name(cls,store_name:str)->"Store":
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls,url_prefix:str)->"Store":
        url_regex = {"$regex":"^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url:str)->"Store":
        """
        Return a store form a url like "https://www.johnlewis.com/item/sdfwfewfw.html"
         :param url: The item's url
         :return: a Store
        """
        print(url)

        pattern = re.findall(r"https?:\/\/.*?\/", url)
        print(pattern[0])
        # match = pattern.search(url)
        # url_prefix = match.group(1)
        return cls.get_by_url_prefix(pattern[0])

        