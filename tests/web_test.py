from dynamicadaptor.DynamicConversion import formate_message
import httpx
import asyncio

async def run():
    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id=749893683697942562"
    headers = {
        "Referer": "https://t.bilibili.com/749893683697942562"
    }
    res = httpx.get(url, headers=headers).json()
    result = await formate_message("web", res["data"]["item"])
    print(result)

if __name__ == "__main__":

    asyncio.run(run())
