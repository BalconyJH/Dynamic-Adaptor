from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel


# goods
class GoodsItem(BaseModel):
    cover: str
    price: str
    name: str

    

class Goods(BaseModel):
    head_text: str
    items: List[GoodsItem]


# Reserve
class ReserveDesc(BaseModel):
    text: str


class Reserve(BaseModel):
    title: str
    desc1: ReserveDesc
    desc2: ReserveDesc


# Common
class Common(BaseModel):
    sub_type: str
    head_text: Optional[str]
    cover: str
    desc1: str
    desc2: Optional[str]
    title: str


# Ugc
class Ugc(BaseModel):
    cover: str
    title: str
    desc_second: str
    duration: str
    head_text: Optional[str]


# Vote
class Vote(BaseModel):
    desc: str
    join_num: int


# class AdditionalDetail(Enum):
#     """
#     ADDITIONAL_TYPE_GOODS       640021213187407875 / 606639498929226246
#     ADDITIONAL_TYPE_RESERVE     746531123737133065
#     ADDITIONAL_TYPE_UGC         610622978014393724
#     ADDITIONAL_TYPE_VOTE        611702685546788433
#     ADDITIONAL_TYPE_COMMON
#     |__game       638931657286484020
#     |__decoration   638611334350503973
#     |__manga    637737411561914375
#     |__ogv      639534382927839233
#     |__pugv     446619415589621845
#     """
#     goods: Goods
#     reserve: Reserve
#     common: Common
#     ugc: Ugc
#     vote: Vote


class Additional(BaseModel):
    type: str
    goods: Optional[Goods]
    reserve: Optional[Reserve]
    common: Optional[Common]
    ugc: Optional[Ugc]
    vote: Optional[Vote]
