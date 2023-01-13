import asyncio
from bilirpc.api import get_dy_detail
from google.protobuf.json_format import MessageToDict
from dynamicadaptor.DynamicConversion import formate_message
import json

async def run():
    message = await get_dy_detail("744639809120632849")
    result = await formate_message(message_type="grpc", message=MessageToDict(message[0]))
    with open("a.json","w") as f:
        f.write(json.dumps(MessageToDict(message[0])))
    print(result.forward.additional)


if __name__ == "__main__":

    asyncio.run(run())
