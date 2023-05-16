import asyncio
from bilirpc.api import get_dy_detail
from google.protobuf.json_format import MessageToJson,MessageToDict
from dynamicadaptor.DynamicConversion import formate_message
import json

async def run():
    message = await get_dy_detail("795989665061535777")
    result = await formate_message(message_type="grpc", message=json.loads(MessageToJson(message[0])))
    # print(result.text.rich_text_nodes)



if __name__ == "__main__":

    asyncio.run(run())
