from dynamicadaptor.DynamicConversion import formate_message
import httpx
import asyncio

async def run():
    dyn_id = "698569146564083856"
    url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id={dyn_id}&features=itemOpusStyle"
    headers = {
        "referer": f"https://t.bilibili.com/{dyn_id}",
        "origin":"https://t.bilibili.com",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    res = httpx.get(url, headers=headers).json()
    result = await formate_message("web", res["data"]["item"])
    print(result.major.opus)

if __name__ == "__main__":

    asyncio.run(run())
