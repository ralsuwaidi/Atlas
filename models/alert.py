import uuid
from dataclasses import dataclass, field
from typing import Dict

from models.item import Item
from models.model import Model
from models.users import User

from libs.mailgun import Mailgun


@dataclass(eq=False)
class Alert(Model):
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    collection: str = field(init=False, default="alerts")

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "price_limit": self.price_limit,
            "item_id": self.item_id,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(
                f'Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}')
            Mailgun.send_email(
                email=[self.user_email],
                subject=f"Notification for {self.name}",
                text=f"Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address to check your item: {self.item.url}.",
                html=f'<p>Your alert {self.name} has reached a price under {self.price_limit}.</p><p>The latest price is {self.item.price}. Check your item out <a href="{self.item.url}>here</a>.</p>',
            )
