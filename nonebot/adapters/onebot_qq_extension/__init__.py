from typing import List, Type

# from nonebot.adapters.onebot.v12.bot import Bot
from nonebot.adapters.onebot.v12.event import *
from nonebot.adapters.onebot.v12.log import *
from nonebot.adapters.onebot.v12.permission import *

from .adapter import *
from .event import *
from .exception import *
from .message import Message, MessageSegment

ADD_MODELS: List[Type[Event]] = []
for model_name in event.__all__:
    model = getattr(event, model_name)
    if not issubclass(model, Event):
        continue
    ADD_MODELS.append(model)

# 引入扩展event
Adapter.add_custom_model(*ADD_MODELS, impl="qq_extension", platform="qq")
