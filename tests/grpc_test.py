import asyncio
from bilirpc.api import get_dy_detail
from google.protobuf.json_format import MessageToDict
from dynamicadaptor.DynamicConversion import formate_message


async def run():
    message = await get_dy_detail("727260760787386403")
    result = await formate_message(message_type="grpc", message=MessageToDict(message[0]))
    # print(result)


if __name__ == "__main__":

    asyncio.run(run())
