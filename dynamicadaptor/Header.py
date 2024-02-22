from pydantic import BaseModel
from typing import Optional


class OfficialVerify(BaseModel):
    type: int


class Pendant(BaseModel):
    pid: Optional[int] = None
    image: Optional[str] = None
    pendant_name: Optional[str] = None


class Vip(BaseModel):
    status: Optional[int] = None
    type: int
    avatar_subscript: Optional[int] = None


class Head(BaseModel):
    name: str
    mid: int
    face: Optional[str] = None
    pub_time: Optional[str] = None
    pub_ts: Optional[int] = None
    vip: Optional[Vip] = None
    pendant: Optional[Pendant] = None
    official_verify: Optional[OfficialVerify] = None
