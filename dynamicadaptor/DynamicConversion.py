from typing import Union

from .Message import RenderMessage
from .Repost import Forward
from loguru import logger

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
        logger.exception(e)
        return None


async def grpc_formate(message: dict) -> Union[RenderMessage, None]:
    """
    将grpc动态转换成渲染数据类型
    Args:
        message: grpc动态转换成Json后的数据

    Returns: RenderMessage

    """
    message_type = message["cardType"]
    message_id = message["extend"]["dynIdStr"]
    header = await get_grpc_header(message["modules"][0]["moduleAuthor"])
    
    text = await get_grpc_text(message)
    major = await get_grpc_major(message)
    additional = await get_grpc_additional(message)
    forward = await get_grpc_forward(message)
    render_message = RenderMessage(
        message_type=message_type,
        message_id=message_id,
        header=header,
        text=text,
        major=major,
        additional=additional,
        forward=forward,
    )
    return render_message


async def get_grpc_header(module_author: dict) -> dict:
    """获取grpc动态的图片头所需要的信息

    Args:
        module_author (dict): grpc动态中的module_author

    Returns:
        dict: 摘要信息
    """
    author = module_author["author"]
    try:
        author["pub_time"] = module_author["ptimeLabelText"]
    except KeyError:
        author["pub_time"] = None
    except Exception as e:
        logger.exception("error")
    try:
        if author["official"]:
            author["official_verify"] = author["official"]
        else:
            author["official_verify"] = {"type": -1}
    except KeyError:
        author["official_verify"] = {"type": -1}
    except Exception as e:
        logger.exception("error")
    try:
        author["vip"]["type"] = author["vip"]["Type"]
    except KeyError:
        author["vip"] = {"status": 0, "type": 0}
    except Exception as e:
        logger.exception("error")
    try:
        author["vip"]["avatar_subscript"] = author["vip"]["avatarSubscript"]
    except KeyError as e:
        author["vip"]["status"] = 0
        author["vip"]["avatar_subscript"] = 0
    except Exception as e:
        logger.exception("error")
    return author


async def get_grpc_forward_header(message: dict) -> dict:
    """获取grpc动态中关于转发动态的作者的信息

    Args:
        message (dict): 含有所有转发动态的module的动态

    Returns:
        dict: 符合要求的信息
    """
    for i in message["modules"]:
        if i["moduleType"] == "module_author_forward":
            author = i["moduleAuthorForward"]
            return {"name": author["title"][0]["text"],"mid": author["uid"]}


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
                    except Exception as e:
                        pass
                    rich_text_nodes.append(temp)
                text["text"] = plain_text
                text["rich_text_nodes"] = rich_text_nodes
        except Exception:
            logger.exception("error")
            pass
    if text:
        return text
    else:
        return None


async def get_grpc_major(message: dict) -> Union[dict, None]:
    """获取grpc动态的major部分

    Args:
        message (dict): 含有所有module的动态

    Returns:
        Union[dict, None]: 符合要求的信息
    """
    for i in message["modules"]:
        try:
            if i["moduleDynamic"]["type"] == "mdl_dyn_forward":
                continue
        except Exception as e:
            pass
        if i["moduleType"] == "module_dynamic":
            module_dynamic_major_type = i["moduleDynamic"]["type"]
            print(module_dynamic_major_type)
            if module_dynamic_major_type == "mdl_dyn_draw":
                try:
                    return {"type": "MAJOR_TYPE_DRAW", "draw": i["moduleDynamic"]["dynDraw"]}
                except Exception as e:
                    logger.exception("error")
            elif module_dynamic_major_type == "mdl_dyn_archive":
                try:
                    i["moduleDynamic"]["dynArchive"]["duration_text"] = i["moduleDynamic"]["dynArchive"]["coverLeftText1"]
                    if "badge" in i["moduleDynamic"]["dynArchive"]:
                        badge = {
                            "text":i["moduleDynamic"]["dynArchive"]["badge"][0]["text"],
                            "color":i["moduleDynamic"]["dynArchive"]["badge"][0]["textColor"],
                            "bg_color": i["moduleDynamic"]["dynArchive"]["badge"][0]["bgColor"] 
                        }
                        i["moduleDynamic"]["dynArchive"]["badge"] = badge
                    return {"type": "MAJOR_TYPE_ARCHIVE", "archive": i["moduleDynamic"]["dynArchive"]}
                except Exception as e:
                    logger.exception("error")
            elif module_dynamic_major_type == "mdl_dyn_live_rcmd":       
                try:
                    return {"type": "MAJOR_TYPE_LIVE_RCMD", "live_rcmd": i["moduleDynamic"]["dynLiveRcmd"]}
                except Exception as e:
                    logger.exception("error")
            elif module_dynamic_major_type == "mdl_dyn_article":
                try:
                    i["moduleDynamic"]["dynArticle"]["cover"] = i["moduleDynamic"]["dynArticle"]["covers"]
                    return {"type": "MAJOR_TYPE_ARTICLE", "article": i["moduleDynamic"]["dynArticle"]}
                except Exception as e:
                    logger.exception("error")
            elif module_dynamic_major_type == "mdl_dyn_common":
                try:
                    i["moduleDynamic"]["dynCommon"]["biz_type"] = i["moduleDynamic"]["dynCommon"]["bizType"]
                    i["moduleDynamic"]["dynCommon"]["url"] = i["moduleDynamic"]["dynCommon"]["uri"]
                    if "badge" in i["moduleDynamic"]["dynCommon"]:
                        badge = {"text":i["moduleDynamic"]["dynCommon"]["badge"][0]["text"],
                        "color":i["moduleDynamic"]["dynCommon"]["badge"][0]["textColor"],
                        "bg_color":i["moduleDynamic"]["dynCommon"]["badge"][0]["bgColor"]}
                        i["moduleDynamic"]["dynCommon"]["badge"] = badge
                    return {"type": "MAJOR_TYPE_COMMON", "common": i["moduleDynamic"]["dynCommon"]}
                except Exception as e:
                    logger.exception("error")
            elif module_dynamic_major_type == "mdl_dyn_music":
                try:
                    i["moduleDynamic"]["dynMusic"]["label"] = i["moduleDynamic"]["dynMusic"]["label1"]
                    return {"type": "MAJOR_TYPE_MUSIC", "music": i["moduleDynamic"]["dynMusic"]}
                except Exception as e:
                    logger.exception("error")
            elif module_dynamic_major_type == "mdl_dyn_pgc":
                try:
                    i["moduleDynamic"]["dynPgc"]["badge"] = {
                        "text": i["moduleDynamic"]["dynPgc"]["badgeCategory"][1]["text"],
                        "color": i["moduleDynamic"]["dynPgc"]["badgeCategory"][1]["textColor"],
                        "bg_color": i["moduleDynamic"]["dynPgc"]["badgeCategory"][1]["bgColor"]}

                    i["moduleDynamic"]["dynPgc"]["stat"] = {"danmaku": i["moduleDynamic"]["dynPgc"]["coverLeftText3"],
                                                            "play": i["moduleDynamic"]["dynPgc"]["coverLeftText2"]}
                    return {"type": "MAJOR_TYPE_PGC", "pgc": i["moduleDynamic"]["dynPgc"]}
                except Exception as e:
                    logger.exception("error")
            elif module_dynamic_major_type == "mdl_dyn_medialist":
                try:
                    i["moduleDynamic"]["dynMedialist"]["sub_title"] = i["moduleDynamic"]["dynMedialist"]["subTitle"]
                    i["moduleDynamic"]["dynMedialist"]["badge"]["color"] = '#FFFFFF'
                    i["moduleDynamic"]["dynMedialist"]["badge"]["bg_color"] = '#FB7299'
                    return {"type": "MAJOR_TYPE_MEDIALIST", "medialist": i["moduleDynamic"]["dynMedialist"]}
                except Exception as e:
                    logger.exception("error")
            elif module_dynamic_major_type == "mdl_dyn_cour_season":
                try:
                    i["moduleDynamic"]["dynCourSeason"]["sub_title"] = i["moduleDynamic"]["dynCourSeason"]["text1"]
                    i["moduleDynamic"]["dynCourSeason"]["badge"]["color"] = '#ffffff'
                    i["moduleDynamic"]["dynCourSeason"]["badge"]["bg_color"] = '#FB7199'
                    return {"type": "MAJOR_TYPE_COURSES", "courses": i["moduleDynamic"]["dynCourSeason"]}
                except Exception as e:
                    logger.exception("error")
            elif module_dynamic_major_type == "mdl_dyn_live":
                try:
                    i["moduleDynamic"]["dynCommonLive"]["desc_first"] = i["moduleDynamic"]["dynCommonLive"]["coverLabel"]
                    if "coverLabel2" in  i["moduleDynamic"]["dynCommonLive"]:
                        i["moduleDynamic"]["dynCommonLive"]["desc_second"] = i["moduleDynamic"]["dynCommonLive"]["coverLabel2"]
                    i["moduleDynamic"]["dynCommonLive"]["badge"]["color"] = '#ffffff'
                    i["moduleDynamic"]["dynCommonLive"]["badge"]["bg_color"] = '#FB7199'
                    return {"type": "MAJOR_TYPE_LIVE", "live": i["moduleDynamic"]["dynCommonLive"]}
                except Exception as e:
                    logger.exception("error")
            else:
                return None
    return None


async def get_grpc_additional(message: dict) -> Union[dict, None]:
    """获取grpc动态的additional部分信息

    Args:
        message (dict): 含有所有module的动态信息

    Returns:
        Union[dict, None]: 符合要求的信息
    """
    for i in message["modules"]:
        if i["moduleType"] == "module_additional":
            try:
                if i["moduleAdditional"]["type"] == "additional_type_up_reservation":
                    reserve = {"title": i["moduleAdditional"]["up"]["title"],
                               "desc1": i["moduleAdditional"]["up"]["descText1"],
                               "desc2": {"text": i["moduleAdditional"]["up"]["descText2"]}}
                    if "descText3" in i["moduleAdditional"]["up"]:
                        reserve["desc3"] = i["moduleAdditional"]["up"]["descText3"]
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
                    except Exception:
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
            except Exception:
                return None
    return None


async def get_grpc_forward(message: dict) -> Union[Forward, None]:
    """获取grpc动态中转发部分的信息

    Args:
        message (dict): 含有所有module的动态信息

    Returns:
        Union[Forward, None]: 符合要求的信息
    """
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
    message_id = message["id_str"]
    major = message["modules"]["module_dynamic"]["major"]
    additional = message["modules"]["module_dynamic"]["additional"]
    try:
        forward_type = message["orig"]["type"]
        forward_header = message["orig"]["modules"]["module_author"]
        try:
            forward_major = message["orig"]["modules"]["module_dynamic"]["major"]
        except KeyError:
            forward_major = None
        except TypeError:
            forward_major = None
        except Exception as e:
            forward_major = None
            logger.exception("error")
        forward_additional = message["orig"]["modules"]["module_dynamic"]["additional"]
        forward_text = message["orig"]["modules"]["module_dynamic"]["desc"]
        if message["orig"]["modules"]["module_dynamic"]["topic"] is not None:
            if forward_text:
                forward_text["topic"] = message["orig"]["modules"]["module_dynamic"]["topic"]
            else:
                forward_text = {"topic":message["orig"]["modules"]["module_dynamic"]["topic"]}
                
        
        forward = Forward(header=forward_header, message_type=forward_type, major=forward_major,
                          additional=forward_additional, text=forward_text)
    except KeyError:
        forward = None

    except TypeError:
        forward = None
        logger.exception("error")

    try:
        text = message["modules"]["module_dynamic"]["desc"]
        if text:
            text["topic"] = message["modules"]["module_dynamic"]["topic"]
        else:
            text = None
    except KeyError:
        text = None

    except TypeError:
        text = None

    except Exception as e:
        text=None
        logger.exception("error")


    render_message = RenderMessage(
        message_type=message["type"],
        message_id=message_id,
        header=header,
        text=text,
        major=major,
        additional=additional,
        forward=forward,
    )

    return render_message
