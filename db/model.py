import datetime
from dataclasses import dataclass

from db.config import Manager


@dataclass
class Customer(Manager):
    id :int = None
    user_id :int = None
    name : str = None
    contact : str = None


@dataclass
class Developer(Manager):
    id :int = None
    user_id :int = None
    name : str = None
    contact : str = None
    occupation : str = None
    tg_username : str = None


@dataclass
class Project(Manager):
    id : int = None
    name : str = None
    description : str = None
    price : int = None
    tz_file : str = None
    due_date : str = None
    occupation_type : str = None
    user_id : int = None
    created_at : datetime = None
    developer_id :int = None