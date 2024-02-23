from pydantic import BaseModel

from .AddonCard import Additional
from .Content import Text
from .Header import Head, Optional
from .Majors import Major


class Forward(BaseModel):
    message_type: str
    header: Head
    text: Optional[Text] = None
    major: Optional[Major] = None
    additional: Optional[Additional] = None
