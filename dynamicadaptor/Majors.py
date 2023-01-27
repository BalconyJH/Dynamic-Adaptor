from typing import List, Optional

from pydantic import BaseModel, Json


# 图片
class DrawItem(BaseModel):
    height: int
    width: int
    src: str


class Draw(BaseModel):
    items: List[DrawItem]


# 视频
class Badge(BaseModel):
    text: Optional[str]
    color: Optional[str]
    bg_color: Optional[str]


class Archive(BaseModel):
    cover: str
    title: str
    desc: Optional[str]
    badge: Optional[Badge]
    duration_text: str


# 直播
class WatchShow(BaseModel):
    text_large:str


class LivePlayInfo(BaseModel):
    title: str
    cover: str
    watched_show:WatchShow


class LiveRcmdContent(BaseModel):
    live_play_info: LivePlayInfo


class LiveRcmd(BaseModel):
    content: Json[LiveRcmdContent]


# 专栏
class Article(BaseModel):
    covers: List[str]
    title: str
    desc: str
    label: str


# common
class Common(BaseModel):
    """
    |_biz_type
      |_0     活动       746596561856757763
      |_3     装扮       551309621391003098
      |_111   分享的游戏  746597347842064405
      |_131   歌单       639296660796604438
      |_141   频道       693101678851784753
      |_231   挂件       746598069396570185
      |_212   话题分享    746597704318058512
    """
    biz_type: int
    badge: Optional[Badge]
    cover: Optional[str]
    desc: Optional[str]
    title: Optional[str]


# 音乐
class Music(BaseModel):
    cover: str
    label: str
    title: str


# pgc
class Stat(BaseModel):
    danmaku: str
    play: str


class Pgc(BaseModel):
    badge: Badge
    cover: str
    title: str
    stat: Stat


# MediaList
class MediaList(BaseModel):
    badge: Badge
    cover: str
    title: str
    sub_title: str


# COURSES
class Courses(BaseModel):
    badge: Badge
    cover: str
    desc: str
    title: str
    sub_title: str


# Live
class Live(BaseModel):
    badge: Badge
    cover: str
    desc_first: str
    desc_second: Optional[str]
    title: str

class UgcSeason(BaseModel):
    title:str
    cover:str
    duration_text:str
    desc:Optional[str]
    stat:Optional[Stat]
    badge:Optional[Badge]



# class MajorDetail(Enum):
#     """
#     类型          动态类型        示例动态
#     draw         图片            741262186696933397
#     archive      视频            739851131027456201
#     live_rcmd    直播
#     ugc_season    合集           755703296984875092 
#     article      专栏            720929682647679043
#     common     装扮 活动等        551309621391003098/743181895357956118
#     music       音乐             692040384055869478
#     pgc         电影/电视剧等     633983562923638785
#     medialist   收藏列表          645144864359448578
#     courses     课程             440646043801479846
#     live        转发直播          727260760787386403
#     """


class Major(BaseModel):
    type: str
    draw: Optional[Draw]
    archive: Optional[Archive]
    live_rcmd: Optional[LiveRcmd]
    article: Optional[Article]
    common: Optional[Common]
    music: Optional[Music]
    pgc: Optional[Pgc]
    medialist: Optional[MediaList]
    courses: Optional[Courses]
    live: Optional[Live]
    ugc_season: Optional[UgcSeason]
