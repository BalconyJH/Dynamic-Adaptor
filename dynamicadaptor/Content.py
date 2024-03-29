from pydantic import BaseModel
from typing import Optional, List, Union


class Emoji(BaseModel):
    icon_url: Optional[str] = None
    text: Optional[str] = None
    type: Union[int, str, None] = None


class RichTextDetail(BaseModel):
    type: str
    text: str
    orig_text: Optional[str] = None
    emoji: Optional[Emoji] = None
    # RICH_TEXT_NODE_TYPE_TEXT      文本
    # RICH_TEXT_NODE_TYPE_AT        At
    # RICH_TEXT_NODE_TYPE_VOTE      投票
    # RICH_TEXT_NODE_TYPE_TOPIC     话题
    # RICH_TEXT_NODE_TYPE_BV        Bv转视频
    # RICH_TEXT_NODE_TYPE_WEB       网页链接
    # RICH_TEXT_NODE_TYPE_LOTTERY   抽奖
    # RICH_TEXT_NODE_TYPE_GOODS     恰饭 640021213187407875
    # RICH_TEXT_NODE_TYPE_EMOJI     bili_emoji


class Topic(BaseModel):
    name: str


class Text(BaseModel):
    text: Optional[str] = None
    topic: Optional[Topic] = None
    rich_text_nodes: Optional[List[RichTextDetail]] = None
