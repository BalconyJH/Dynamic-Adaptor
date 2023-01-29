import asyncio
from bilirpc.api import get_dy_detail
from google.protobuf.json_format import MessageToJson,MessageToDict
from dynamicadaptor.DynamicConversion import formate_message
import json

async def run():
    message = await get_dy_detail("756200529630068741")
    result = await formate_message(message_type="grpc", message=json.loads(MessageToJson(message[0])))
    # with open("a.json","w") as f:
    #     f.write(MessageToJson(message[0]))
    print(result.major)



if __name__ == "__main__":

    asyncio.run(run())
