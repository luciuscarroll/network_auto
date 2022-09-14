from lib2to3.pgen2.token import OP
from typing import Optional
from sqlmodel import SQLModel, Field

class Users (SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    mac_address: Optional[str]

class Radreply (SQLModel, table=True):
    __tablename__ = "radreply"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    
class Radcheck (SQLModel, table=True):
    __tablename__ = "radcheck"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str









