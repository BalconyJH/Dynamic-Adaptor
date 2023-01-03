from typing import Union

from .Message import RenderMessage
from .Repost import Forward


async def formate_message(message_type: str, message: dict) -> Union[None, RenderMessage]:
    """将grpc动态或web端动态转换成渲染数据类型

    Args:
        message_type (str): "grpc" or "web"
        message (dict): 对于动态内的item

    Returns:
        Union[None, RenderMessage]: 渲染数据类型
    """
    try:
        if message_type == "grpc":
            return await grpc_formate(message)
        elif message_type == "web":
            return await web_formate(message)
        else:
            return None
    except Exception as e:
        return None


async def grpc_formate(message: dict) -> Union[RenderMessage, None]:
    """
    将grpc动态转换成渲染数据类型
    Args:
        message: grpc动态转换成Json后的数据

    Returns: RenderMessage

    """
    message_type = message["cardType"]
    header = await get_grpc_header(message["modules"][0]["moduleAuthor"])
    text = await get_grpc_text(message)
    major = await get_grpc_major(message)
    additional = await get_grpc_additional(message)
    forward = await get_grpc_forward(message)
    render_message = RenderMessage(
        message_type=message_type,
        header=header,
        text=text,
        major=major,
        additional=additional,
        forward=forward,
    )
    return render_message


async def get_grpc_header(module_author: dict) -> dict:
    author = module_author["author"]
    try:
        author["pub_time"] = module_author["ptimeLabelText"]
    except KeyError:
        author["pub_time"] = None
    try:
        if author["official"]:
            author["official_verify"] = author["official"]
        else:
            author["official_verify"] = {"type": -1}
    except KeyError:
        author["official_verify"] = {"type": -1}
    try:
        author["vip"]["type"] = author["vip"]["Type"]
    except KeyError:
        author["vip"] = {"status": 0, "type": 0}

    try:
        author["vip"]["avatar_subscript"] = author["vip"]["avatarSubscript"]
    except KeyError as e:
        author["vip"]["status"] = 0
        author["vip"]["avatar_subscript"] = 0
    return author


async def get_grpc_forward_header(message: dict) -> dict:
    for i in message["modules"]:
        if i["moduleType"] == "module_author_forward":
            author = i["moduleAuthorForward"]
            return {"name": author["title"][0]["text"]}


async def get_grpc_text(message: dict) -> Union[dict, None]:
    """
    将grpc动态的文字部分的类型转换成渲染需要的统一类型
    Args:
        message: 动态

    Returns: 文本部分

    """
    text = {}
    rich_type_dict = {"desc_type_text": "RICH_TEXT_NODE_TYPE_TEXT",
                      "desc_type_aite": "RICH_TEXT_NODE_TYPE_AT",
                      "desc_type_vote": "RICH_TEXT_NODE_TYPE_VOTE",
                      "desc_type_topic": "RICH_TEXT_NODE_TYPE_TOPIC",
                      "desc_type_bv": "RICH_TEXT_NODE_TYPE_BV",
                      "desc_type_web": "RICH_TEXT_NODE_TYPE_WEB",
                      "desc_type_lottery": "RICH_TEXT_NODE_TYPE_LOTTERY",
                      "desc_type_goods": "RICH_TEXT_NODE_TYPE_GOODS",
                      "desc_type_emoji": "RICH_TEXT_NODE_TYPE_EMOJI"
                      }
    for i in message["modules"]:
        try:
            if i["moduleType"] == "module_topic":
                text["topic"] = i["moduleTopic"]
        except:
            pass
        try:
            if i["moduleType"] == "module_desc":
                plain_text = i["moduleDesc"]["text"]
                rich_text_nodes = []
                for j in i["moduleDesc"]["desc"]:
                    temp = {"type": rich_type_dict[j["type"]], "text": j["text"], "orig_text": j["origText"]}
                    try:
                        temp["emoji"] = {"icon_url": j["uri"], "type": j["emojiType"], "text": j["text"]}
                    except KeyError as e:
                        pass
                    rich_text_nodes.append(temp)
                text["text"] = plain_text
                text["rich_text_nodes"] = rich_text_nodes
        except KeyError:
            pass
    if text:
        return text
    else:
        return None


async def get_grpc_major(message: dict) -> Union[dict, None]:
    for i in message["modules"]:
        try:
            if i["moduleDynamic"]["type"] == "mdl_dyn_forward":
                continue
        except KeyError:
            pass
        if i["moduleType"] == "module_dynamic":
            try:
                return {"type": "MAJOR_TYPE_DRAW", "draw": i["moduleDynamic"]["dynDraw"]}
            except KeyError:
                pass
            try:
                i["moduleDynamic"]["dynArchive"]["duration_text"] = i["moduleDynamic"]["dynArchive"]["coverLeftText1"]
                return {"type": "MAJOR_TYPE_ARCHIVE", "archive": i["moduleDynamic"]["dynArchive"]}
            except KeyError:
                pass
            try:
                return {"type": "MAJOR_TYPE_LIVE_RCMD", "live_rcmd": i["moduleDynamic"]["dynLiveRcmd"]}
            except KeyError:
                pass
            try:
                i["moduleDynamic"]["dynArticle"]["cover"] = i["moduleDynamic"]["dynArticle"]["covers"]
                return {"type": "MAJOR_TYPE_ARTICLE", "article": i["moduleDynamic"]["dynArticle"]}
            except KeyError:
                pass
            try:
                i["moduleDynamic"]["dynCommon"]["biz_type"] = i["moduleDynamic"]["dynCommon"]["bizType"]
                i["moduleDynamic"]["dynCommon"]["url"] = i["moduleDynamic"]["dynCommon"]["uri"]
                return {"type": "MAJOR_TYPE_COMMON", "common": i["moduleDynamic"]["dynCommon"]}
            except KeyError:
                pass
            pass
            try:
                i["moduleDynamic"]["dynMusic"]["label"] = i["moduleDynamic"]["dynMusic"]["label1"]
                return {"type": "MAJOR_TYPE_MUSIC", "music": i["moduleDynamic"]["dynMusic"]}
            except KeyError:
                pass
            try:
                i["moduleDynamic"]["dynPgc"]["badge"] = {
                    "text": i["moduleDynamic"]["dynPgc"]["badgeCategory"][1]["text"],
                    "color": i["moduleDynamic"]["dynPgc"]["badgeCategory"][1]["textColor"],
                    "bg_color": i["moduleDynamic"]["dynPgc"]["badgeCategory"][1]["bgColor"]}

                i["moduleDynamic"]["dynPgc"]["stat"] = {"danmaku": i["moduleDynamic"]["dynPgc"]["coverLeftText3"],
                                                        "play": i["moduleDynamic"]["dynPgc"]["coverLeftText2"]}
                return {"type": "MAJOR_TYPE_PGC", "pgc": i["moduleDynamic"]["dynPgc"]}
            except KeyError:
                pass
            try:
                i["moduleDynamic"]["dynMedialist"]["sub_title"] = i["moduleDynamic"]["dynMedialist"]["subTitle"]
                i["moduleDynamic"]["dynMedialist"]["badge"]["color"] = '#FFFFFF'
                i["moduleDynamic"]["dynMedialist"]["badge"]["bg_color"] = '#FB7299'
                return {"type": "MAJOR_TYPE_MEDIALIST", "medialist": i["moduleDynamic"]["dynMedialist"]}
            except KeyError:
                pass
            try:
                i["moduleDynamic"]["dynCourSeason"]["sub_title"] = i["moduleDynamic"]["dynCourSeason"]["text1"]
                i["moduleDynamic"]["dynCourSeason"]["badge"]["color"] = '#ffffff'
                i["moduleDynamic"]["dynCourSeason"]["badge"]["bg_color"] = '#FB7199'
                return {"type": "MAJOR_TYPE_COURSES", "courses": i["moduleDynamic"]["dynCourSeason"]}
            except KeyError:
                pass
            try:
                i["moduleDynamic"]["dynCommonLive"]["desc_first"] = i["moduleDynamic"]["dynCommonLive"]["coverLabel"]
                i["moduleDynamic"]["dynCommonLive"]["desc_second"] = i["moduleDynamic"]["dynCommonLive"]["coverLabel2"]
                i["moduleDynamic"]["dynCourSeason"]["badge"]["color"] = '#ffffff'
                i["moduleDynamic"]["dynCourSeason"]["badge"]["bg_color"] = '#FB7199'
                return {"type": "MAJOR_TYPE_LIVE", "live": i["moduleDynamic"]["dynCommonLive"]}
            except KeyError:
                pass
            return None
    return None


async def get_grpc_additional(message: dict) -> Union[dict, None]:
    for i in message["modules"]:
        if i["moduleType"] == "module_additional":
            try:
                if i["moduleAdditional"]["type"] == "additional_type_up_reservation":
                    reserve = {"title": i["moduleAdditional"]["up"]["title"],
                               "desc1": i["moduleAdditional"]["up"]["descText1"],
                               "desc2": {"text": i["moduleAdditional"]["up"]["descText2"]}}
                    return {"type": "ADDITIONAL_TYPE_RESERVE", "reserve": reserve}
                elif i["moduleAdditional"]["type"] == "additional_type_goods":
                    items = []
                    for j in i["moduleAdditional"]["goods"]["goodsItems"]:
                        j["name"] = j["title"]
                        items.append(j)
                    goods = {
                        "head_text": i["moduleAdditional"]["goods"]["rcmdDesc"],
                        "items": items
                    }
                    return {"type": "ADDITIONAL_TYPE_GOODS", "goods": goods}
                elif i["moduleAdditional"]["type"] == "additional_type_common":
                    try:
                        head_text = i["moduleAdditional"]["common"]["headText"]
                    except KeyError:
                        head_text = None
                    common = {
                        "head_text": head_text,
                        "sub_type": i["moduleAdditional"]["common"]["cardType"],
                        "cover": i["moduleAdditional"]["common"]["imageUrl"],
                        "title": i["moduleAdditional"]["common"]["title"],
                        "desc1": i["moduleAdditional"]["common"]["descText1"],
                        "desc2": i["moduleAdditional"]["common"]["descText2"]
                    }
                    return {"type": "ADDITIONAL_TYPE_COMMON", "common": common}
                elif i["moduleAdditional"]["type"] == "additional_type_ugc":
                    i["moduleAdditional"]["ugc"]["desc_second"] = i["moduleAdditional"]["ugc"]["descText2"]
                    return {"type": "ADDITIONAL_TYPE_UGC", "ugc": i["moduleAdditional"]["ugc"]}
                elif i["moduleAdditional"]["type"] == "additional_type_vote":
                    vote = {
                        "desc": i["moduleAdditional"]["vote2"]["title"],
                        "join_num": i["moduleAdditional"]["vote2"]["total"]
                    }
                    return {"type": "ADDITIONAL_TYPE_VOTE", "vote": vote}

            except Exception as e:
                return None
    return None


async def get_grpc_forward(message: dict) -> Union[Forward, None]:
    dynamic_forward = None
    for i in message["modules"]:
        try:
            module_type = i["moduleDynamic"]["type"]
            if i["moduleType"] == "module_dynamic" and module_type == "mdl_dyn_forward":
                dynamic_forward = i["moduleDynamic"]["dynForward"]["item"]
                break
        except Exception as e:
            continue
    if dynamic_forward:
        forward_message_type = dynamic_forward["cardType"]
        forward_header = await get_grpc_forward_header(dynamic_forward)
        forward_major = await get_grpc_major(dynamic_forward)
        forward_text = await get_grpc_text(dynamic_forward)
        forward_additional = await get_grpc_additional(dynamic_forward)
        forward = Forward(
            message_type=forward_message_type,
            header=forward_header,
            text=forward_text,
            major=forward_major,
            additional=forward_additional
        )
        return forward
    else:
        return None


async def web_formate(message: dict) -> RenderMessage:
    """
    将web返回的动态的item格式化成为render所需的数据类型
    Args:
        message: web动态的item

    Returns: RenderMessage

    """
    header = message["modules"]["module_author"]
    major = message["modules"]["module_dynamic"]["major"]
    additional = message["modules"]["module_dynamic"]["additional"]
    try:
        forward_type = message["orig"]["type"]
        forward_header = message["orig"]["modules"]["module_author"]
        try:
            forward_major = message["orig"]["modules"]["module_dynamic"]["major"]
        except KeyError:
            forward_major = None
        forward_additional = message["orig"]["modules"]["module_dynamic"]["additional"]
        forward_text = message["orig"]["modules"]["module_dynamic"]["desc"]
        forward = Forward(header=forward_header, message_type=forward_type, major=forward_major,
                          additional=forward_additional, text=forward_text)
    except KeyError:
        forward = None
    try:
        text = message["modules"]["module_dynamic"]["desc"]
        text["topic"] = message["modules"]["module_dynamic"]["topic"]
    except KeyError:
        text = None
    render_message = RenderMessage(
        message_type=message["type"],
        header=header,
        text=text,
        major=major,
        additional=additional,
        forward=forward,
    )
    return render_message
