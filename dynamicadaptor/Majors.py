from typing import List, Optional, Union
from pydantic import BaseModel, Json


class DrawItem(BaseModel):
    height: int
    width: int
    src: Optional[str] = None
    url: Optional[str] = None


class Draw(BaseModel):
    items: List[DrawItem]


class Badge(BaseModel):
    text: Optional[str] = None
    color: Optional[str] = None
    bg_color: Optional[str] = None


class Archive(BaseModel):
    cover: str
    title: str
    desc: Optional[str] = None
    badge: Optional[Badge] = None
    duration_text: str


# 直播
class WatchShow(BaseModel):
    text_large: str


class LivePlayInfo(BaseModel):
    title: str
    cover: str
    watched_show: WatchShow


class LiveRcmdContent(BaseModel):
    live_play_info: LivePlayInfo


class LiveRcmd(BaseModel):
    content: Json[LiveRcmdContent]


class Article(BaseModel):
    covers: List[str]
    title: str
    desc: str
    label: str


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
    badge: Optional[Badge] = None
    cover: Optional[str] = None
    desc: Optional[str] = None
    title: Optional[str] = None


class Music(BaseModel):
    cover: str
    label: str
    title: str


class Stat(BaseModel):
    danmaku: str
    play: str


class Pgc(BaseModel):
    badge: Badge
    cover: str
    title: str
    stat: Stat


class MediaList(BaseModel):
    badge: Badge
    cover: str
    title: str
    sub_title: str


class Courses(BaseModel):
    badge: Badge
    cover: str
    desc: str
    title: str
    sub_title: str


class Live(BaseModel):
    badge: Badge
    cover: str
    desc_first: str
    desc_second: Optional[str] = None
    title: str


class UgcSeason(BaseModel):
    title: str
    cover: str
    duration_text: str
    desc: Optional[str] = None
    stat: Optional[Stat] = None
    badge: Optional[Badge] = None


class MNone(BaseModel):
    tips: str


class Emoji(BaseModel):
    icon_url: Optional[str] = None
    text: Optional[str] = None
    type: Union[int, str, None] = None


class RichTextNodes(BaseModel):
    type: str
    text: str
    orig_text: Optional[str] = None
    emoji: Optional[Emoji] = None


class Summary(BaseModel):
    text: str
    rich_text_nodes: List[RichTextNodes]


class OPUS(BaseModel):
    pics: Optional[List[DrawItem]] = None
    summary: Optional[Summary] = None
    title: Optional[str] = None

# class MajorDetail(Enum):
#     """
#     类型          动态类型        示例动态
#     draw         图片            741262186696933397
#     archive      视频            739851131027456201
#     live_rcmd    直播
#     ugc_season    合集           755703296984875092 
#     article      专栏            819930757423169558
#     common     装扮 活动等        551309621391003098/743181895357956118
#     music       音乐             819725994851041346
#     pgc         电影/电视剧等     633983562923638785
#     medialist   收藏列表          645144864359448578
#     courses     课程             440646043801479846
#     live        转发直播          727260760787386403
#     """

class BgImage(BaseModel):
    img_dark: str
    img_day: str


class Button(BaseModel):
    icon: Optional[str] = None
    text: Optional[str] = None


class Blocked(BaseModel):
    hint_message: Optional[str] = None
    blocked_type: int
    bg_img: Optional[BgImage] = None
    icon: Optional[BgImage] = None


class Major(BaseModel):
    type: str
    draw: Optional[Draw] = None
    archive: Optional[Archive] = None
    live_rcmd: Optional[LiveRcmd] = None
    article: Optional[Article] = None
    common: Optional[Common] = None
    music: Optional[Music] = None
    pgc: Optional[Pgc] = None
    medialist: Optional[MediaList] = None
    courses: Optional[Courses] = None
    live: Optional[Live] = None
    ugc_season: Optional[UgcSeason] = None
    opus: Optional[OPUS] = None
    none: Optional[MNone] = None
    blocked: Optional[Blocked] = None
