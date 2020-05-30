import uuid
from dataclasses import dataclass, field
from typing import Dict, List
from models.model import Model
from common.database import Database
from common.utils import Utils
import models.users.errors as UserErrors

@dataclass
class User(Model):
    collection: str = field(init=False, default='users')
    email:str
    password:str
    _id:str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email:str)->"User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this e-mail was not found')

    @classmethod
    def is_login_valid(cls, email:str,password:str)->bool:
        user = cls.find_by_email(email)

        if not Utils.check_hashed_password(password, user.password):
            raise UserErrors.IncorrectPasswordError('Your password is incorrect.')

        return True
    @classmethod
    def register_user(cls, email:str, password:str) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('This email does not have the proper format')

        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError('A user with this email already exists')
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_mongo()

        return True

    def json(self)->Dict:
        return {
            "_id":self._id,
            "email":self.email,
            "password":self.password
        }