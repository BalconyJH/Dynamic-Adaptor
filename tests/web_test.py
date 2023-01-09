from dynamicadaptor.DynamicConversion import formate_message
import httpx
import asyncio

async def run():
    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id=749088866961457157"
    headers = {
        "Referer": "https://t.bilibili.com/749088866961457157"
    }
    res = httpx.get(url, headers=headers).json()
    result = await formate_message("web", res["data"]["item"])
    print(result.forward.text.topic)

if __name__ == "__main__":

    asyncio.run(run())
