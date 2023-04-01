from dynamicadaptor.DynamicConversion import formate_message
import httpx
import asyncio

async def run():
    # dyn_id = "75570329698487509"
    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id=779490646924722209&features=itemOpusStyle"
    headers = {
        "referer": "https://t.bilibili.com/779490646924722209",
        "origin":"https://t.bilibili.com"
    }
    res = httpx.get(url, headers=headers).json()
    # print(res)
    result = await formate_message("web", res["data"]["item"])
    print(result.forward.additional)

if __name__ == "__main__":

    asyncio.run(run())
