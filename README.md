
# DynamicAdaptor
-------------

用于将bilibili的grpc动态和web动态转换成特定的数据类型


### 原理说明
将grpc数据转换成json数据，之后使用pydantic进行信息摘要。
web端的json数据同理


### 下载安装
``` xml
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



## License
GPL
