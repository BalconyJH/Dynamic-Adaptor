from pydantic import BaseModel

from .AddonCard import Additional
from .Content import Text
from .Header import Head, Optional
from .Majors import Major
from .Repost import Forward


class RenderMessage(BaseModel):
    message_type: str
    message_id: str
    header: Head
    text: Optional[Text] = None
    major: Optional[Major] = None
    additional: Optional[Additional] = None
    forward: Optional[Forward] = None
