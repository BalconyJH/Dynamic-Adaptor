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
