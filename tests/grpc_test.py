import asyncio
from bilirpc.api import get_dy_detail
from google.protobuf.json_format import MessageToJson,MessageToDict
from dynamicadaptor.DynamicConversion import formate_message
import json

async def run():
    message = await get_dy_detail("751145855632801799")
    result = await formate_message(message_type="grpc", message=json.loads(MessageToJson(message[0])))
    # with open("a.json","w") as f:
    #     f.write(json.dumps(MessageToDict(message[0])))
    print(result)


if __name__ == "__main__":

    asyncio.run(run())
