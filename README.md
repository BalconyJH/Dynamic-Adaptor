
# DynamicAdaptor

-------------

用于将bilibili的grpc动态和web动态转换成特定的数据类型

### 原理说明

将grpc数据转换成json数据，之后使用pydantic进行信息摘要。
web端的json数据同理

### 下载安装

```bash
pip install dynamicadaptor
```

### 使用方法

```python

from google.protobuf.json_format import MessageToDict
from dynamicadaptor.DynamicConversion import formate_message
from bilirpc.api import get_dy_detail
import asyncio
import httpx


# 如果数据是grpc返回的数据，则需要转换成json数据
async def sample1():
    dynamic_grpc = await get_dy_detail("746530608345251842")
    dynamic: dict = MessageToDict(dynamic_grpc[0])
    dynamic_formate =await formate_message("grpc", dynamic)
    print(dynamic_formate)


asyncio.run(sample1())


# 如果是web返回的数据
async def sample2():
    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id=746530608345251842"
    headers = {
        "Referer": "https://t.bilibili.com/746530608345251842"
    }
    result = httpx.get(url, headers=headers).json()
    dynamic_formate =await formate_message("web", result["data"]["item"])
    print(dynamic_formate)


asyncio.run(sample2())




```

## 数据结构

```bash
message
├─message_type: str
├─message_id:str
├─header: Head
|   ├─name: str
|   ├─mid: int
|   ├─face: Optional[str]  
|   ├─pub_time: Optional[str]
|   ├─pub_ts: Optional[int]
|   ├─vip: Optional
|   |   ├─status: Optional[int]
|   |   ├─type: int
|   |   └─vatar_subscript: Optional[int]
|   |
|   ├─pendant: Optional
|   |   ├─pid: Optional[int]
|   |   ├─image: Optional[str]
|   |   └─pendant_name: Optional[str]
|   └─official_verify: Optional
|      └─type: int
├─text: Optional
|   ├─text: Optional
|   ├─topic: Optional
|   |   └─name: str
|   └─rich_text_nodes:Optional[List[RichTextDetail]]
|      ├─type: str
|      ├─text: str
|      ├─orig_text: Optional[str]
|      └─emoji: Optional
|          ├─icon_url: Optional[str]
|          ├─text: Optional[str]
|          └─type: Union[int, str, None]     
|   
├─major: Optional
|   ├─type: str
|   ├─draw: Optional
|   |   └─items: List
|   |       ├─height: int
|   |       ├─width: int
|   |       └─src: str
|   ├─archive: Optional
|   |   ├─cover: str
|   |   ├─title: str
|   |   ├─desc: Optional[str]
|   |   ├─duration_text: str
|   |   └─badge: Optional
|   |       ├─text: Optional[str]
|   |       ├─color: Optional[str]
|   |       └─bg_color: Optional[str] 
|   ├─live_rcmd: Optional
|   |   └─content: Json
|   |       └─live_play_info
|   |           ├─title: str
|   |           ├─cover: str                  
|   |           └─watched_show
|   |               └─text_large:str
|   ├─article: Optional
|   |   ├─cover: List[str]
|   |   ├─title: str
|   |   ├─desc: str
|   |   └─label: str
|   ├─common: Optional
|   |   ├─biz_type: int
|   |   ├─cover: Optional[str]
|   |   ├─desc: Optional[str]
|   |   ├─title: Optional[str]  
|   |   └─badge: Optional
|   |       ├─text: Optional[str]
|   |       ├─color: Optional[str]
|   |       └─bg_color: Optional[str]
|   ├─music: Optional
|   |   ├─cover: str
|   |   ├─label: str
|   |   └─title: str
|   ├─pgc: Optional
|   |   ├─cover: str
|   |   ├─title: str
|   |   ├─badge
|   |   |   ├─text: Optional[str]
|   |   |   ├─color: Optional[str]
|   |   |   └─bg_color: Optional[str]
|   |   └─stat
|   |       ├─danmaku: str
|   |       └─play: str
|   ├─medialist: Optional
|   |   ├─cover: str
|   |   ├─title: str
|   |   ├─sub_title: str
|   |   └─badge
|   |       ├─text: Optional[str]
|   |       ├─color: Optional[str]
|   |       └─bg_color: Optional[str]
|   ├─courses: Optional
|   |   ├─cover: str
|   |   ├─title: str
|   |   ├─desc: str
|   |   ├─sub_title: str
|   |   └─badge
|   |       ├─text: Optional[str]
|   |       ├─color: Optional[str]
|   |       └─bg_color: Optional[str]
|   └─live
|       ├─cover: str
|       ├─title: str
|       ├─desc_first: str
|       ├─desc_second: str
|       └─badge
|           ├─text: Optional[str]
|           ├─color: Optional[str]
|           └─bg_color: Optional[str]
├─additional: Optional
|   ├─type: str
|   ├─goods: Optional
|   |   ├─head_text: str
|   |   └─items: List
|   |       ├─cover: str
|   |       ├─price: str
|   |       └─name: str
|   ├─reserve: Optional
|   |   ├─title: str
|   |   ├─desc1
|   |   |   └─text: str  
|   |   └─desc2
|   |       └─text: str
|   ├─common
|   |   ├─sub_type: str
|   |   ├─head_text: Optional[str]
|   |   ├─cover: str
|   |   ├─desc1: str
|   |   ├─desc2: Optional[str]
|   |   └─title: str
|   ├─ugc
|   |   ├─cover: str
|   |   ├─title: str
|   |   ├─desc_second: str
|   |   ├─duration: str
|   |   └─head_text: Optional[str]
|   └─vote
|       ├─desc: str
|       └─join_num: int
└─forward: Optional
    ├─message_type: str
    ├─message_id:str
    ├─header: Head
    |   ├─name: str
    |   ├─mid: int
    |   ├─face: Optional[str]  
    |   ├─pub_time: Optional[str]
    |   ├─pub_ts: Optional[int]
    |   ├─vip: Optional
    |   |   ├─status: Optional[int]
    |   |   ├─type: int
    |   |   └─vatar_subscript: Optional[int]
    |   |
    |   ├─pendant: Optional
    |   |   ├─pid: Optional[int]
    |   |   ├─image: Optional[str]
    |   |   └─pendant_name: Optional[str]
    |   └─official_verify: Optional
    |      └─type: int
    ├─text: Optional
    |   ├─text: Optional
    |   ├─topic: Optional
    |   |   └─name: str
    |   └─rich_text_nodes:Optional[List[RichTextDetail]]
    |      ├─type: str
    |      ├─text: str
    |      ├─orig_text: Optional[str]
    |      └─emoji: Optional
    |          ├─icon_url: Optional[str]
    |          ├─text: Optional[str]
    |          └─type: Union[int, str, None]     
    |   
    ├─major: Optional
    |   ├─type: str
    |   ├─draw: Optional
    |   |   └─items: List
    |   |       ├─height: int
    |   |       ├─width: int
    |   |       └─src: str
    |   ├─archive: Optional
    |   |   ├─cover: str
    |   |   ├─title: str
    |   |   ├─desc: Optional[str]
    |   |   ├─duration_text: str
    |   |   └─badge: Optional
    |   |       ├─text: Optional[str]
    |   |       ├─color: Optional[str]
    |   |       └─bg_color: Optional[str] 
    |   ├─live_rcmd: Optional
    |   |   └─content: Json
    |   |       └─live_play_info
    |   |           ├─title: str
    |   |           ├─cover: str                  
    |   |           └─watched_show
    |   |               └─text_large:str
    |   ├─article: Optional
    |   |   ├─cover: List[str]
    |   |   ├─title: str
    |   |   ├─desc: str
    |   |   └─label: str
    |   ├─common: Optional
    |   |   ├─biz_type: int
    |   |   ├─cover: Optional[str]
    |   |   ├─desc: Optional[str]
    |   |   ├─title: Optional[str]  
    |   |   └─badge: Optional
    |   |       ├─text: Optional[str]
    |   |       ├─color: Optional[str]
    |   |       └─bg_color: Optional[str]
    |   ├─music: Optional
    |   |   ├─cover: str
    |   |   ├─label: str
    |   |   └─title: str
    |   ├─pgc: Optional
    |   |   ├─cover: str
    |   |   ├─title: str
    |   |   ├─badge
    |   |   |   ├─text: Optional[str]
    |   |   |   ├─color: Optional[str]
    |   |   |   └─bg_color: Optional[str]
    |   |   └─stat
    |   |       ├─danmaku: str
    |   |       └─play: str
    |   ├─medialist: Optional
    |   |   ├─cover: str
    |   |   ├─title: str
    |   |   ├─sub_title: str
    |   |   └─badge
    |   |       ├─text: Optional[str]
    |   |       ├─color: Optional[str]
    |   |       └─bg_color: Optional[str]
    |   ├─courses: Optional
    |   |   ├─cover: str
    |   |   ├─title: str
    |   |   ├─desc: str
    |   |   ├─sub_title: str
    |   |   └─badge
    |   |       ├─text: Optional[str]
    |   |       ├─color: Optional[str]
    |   |       └─bg_color: Optional[str]
    |   └─live
    |       ├─cover: str
    |       ├─title: str
    |       ├─desc_first: str
    |       ├─desc_second: str
    |       └─badge
    |           ├─text: Optional[str]
    |           ├─color: Optional[str]
    |           └─bg_color: Optional[str]
    └─additional: Optional
        ├─type: str
        ├─goods: Optional
        |   ├─head_text: str
        |   └─items: List
        |       ├─cover: str
        |       ├─price: str
        |       └─name: str
        ├─reserve: Optional
        |   ├─title: str
        |   ├─desc1
        |   |   └─text: str  
        |   └─desc2
        |       └─text: str
        ├─common
        |   ├─sub_type: str
        |   ├─head_text: Optional[str]
        |   ├─cover: str
        |   ├─desc1: str
        |   ├─desc2: Optional[str]
        |   └─title: str
        ├─ugc
        |   ├─cover: str
        |   ├─title: str
        |   ├─desc_second: str
        |   ├─duration: str
        |   └─head_text: Optional[str]
        └─vote
            ├─desc: str
            └─join_num: int
```

## License

GPL
