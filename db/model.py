import datetime
from dataclasses import dataclass

from db.config import Manager

@dataclass
class User(Manager):
    chat_id :int = None
    name : str = None
    contact : str = None
    occupation : str = None
    role : str = None

class Project(Manager):
    id : int = None
    name : str = None
    description : str = None
    price : int = None
    tz_file : str = None
    due_data : datetime = None
    developer_id : int = None
    customer_id : int = None
    created_at : datetime = None
