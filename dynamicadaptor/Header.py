from pydantic import BaseModel
from typing import Optional


class OfficialVerify(BaseModel):
    type: int


class Pendant(BaseModel):
    pid: Optional[int]
    image: Optional[str]
    pendant_name: Optional[str]


class Vip(BaseModel):
    status: Optional[int]
    type: int
    avatar_subscript: Optional[int]


class Head(BaseModel):
    name: str
    mid: int
    face: Optional[str]
    pub_time: Optional[str]
    pub_ts: Optional[int]
    vip: Optional[Vip]
    pendant: Optional[Pendant]
    official_verify: Optional[OfficialVerify]
