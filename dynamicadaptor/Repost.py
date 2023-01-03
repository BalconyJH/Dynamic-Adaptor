from pydantic import BaseModel

from .AddonCard import Additional
from .Content import Text
from .Header import Head, Optional
from .Majors import Major


class Forward(BaseModel):
    message_type: str
    header: Head
    text: Optional[Text]
    major: Optional[Major]
    additional: Optional[Additional]
