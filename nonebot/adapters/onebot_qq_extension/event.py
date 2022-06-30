from nonebot.adapters.onebot.v12 import NoticeEvent, MessageEvent, RequestEvent as BaseRequestEvent
from typing_extensions import Literal

# from nonebot.typing import overrides
from .bot import Bot


class GroupTempMessageEvent(MessageEvent):
    """群临时消息"""

    detail_type: Literal["group_temp"]
    to_me = True
    group_id: str
    """群 ID"""
    user_name: str
    """发送者用户名称/昵称"""


class FriendPokeNotice(NoticeEvent):
    """好友戳一戳通知"""

    detail_type: Literal["friend_poke"]
    user_id: str
    """发送者 ID"""
    receiver_id: str
    """接收者 ID"""


class GroupNameUpdateNotice(NoticeEvent):
    """群名称更新通知"""

    detail_type: Literal["group_name_update"]
    group_id: str
    """群 ID"""
    group_name: str
    """群名称"""
    operator_id: str
    """操作者 ID"""


# 中间继承类
class RequestEvent(BaseRequestEvent):
    """请求事件"""

    request_id: int
    """flag"""

    async def accept(self, bot: "Bot"):
        """同意当前请求"""
        raise ValueError("Request has no accept!")

    async def reject(self, bot: "Bot", block: bool = False, message: str = ""):
        """拒绝当前请求

        Args:
            `bot` (Bot): 处理的Bot
            `block` (bool, optional): 是否禁止再次申请，默认 False
            `message` (str, optional): 拒绝理由，默认 ""
        """
        raise ValueError("Request has no reject!")


class FriendAddRequestEvent(RequestEvent):
    """好友添加请求"""

    detail_type: Literal["new_friend"]
    user_id: str
    user_name: str
    message: str

    async def accept(self, bot: Bot):
        return await bot.set_new_friend(
            request_id=self.request_id,
            user_id=self.user_id,
            accept=True,
        )

    async def reject(self, bot: Bot):
        """拒绝当前请求"""
        return await bot.set_new_friend(
            request_id=self.request_id,
            user_id=self.user_id,
            accept=False,
        )


class GroupJoinRequestEvent(RequestEvent):
    """新成员加群申请请求"""

    detail_type: Literal["join_group"]
    user_id: str
    user_name: str
    group_id: str
    group_name: str
    message: str
    suspicious: bool
    invitor_id: str = None
    invitor_name: str = None

    async def accept(self, bot: "Bot"):
        return await bot.set_join_group(
            request_id=self.request_id,
            user_id=self.user_id,
            group_id=self.group_id,
            accept=True,
        )

    async def reject(self, bot: "Bot", block: bool = False, message: str = ""):
        return await bot.set_join_group(
            request_id=self.request_id,
            user_id=self.user_id,
            group_id=self.group_id,
            accept=False,
            block=block,
            message=message,
        )


class GroupinvItedRequestEvent(RequestEvent):
    """被邀请入群请求"""
    detail_type: str
    group_id: str
    group_name: str
    invitor_id: str = None
    invitor_name: str = None

    async def accept(self, bot: "Bot"):
        return await bot.set_group_invited(
            request_id=self.request_id,
            group_id=self.group_id,
            accept=self.invitor_id,
        )

    async def reject(self, bot: "Bot"):
        """拒绝当前请求"""
        return await bot.set_group_invited(
            request_id=self.request_id,
            group_id=self.group_id,
            accept=False,
        )


__all__ = [
    "GroupTempMessageEvent",
    "FriendPokeNotice",
    "GroupNameUpdateNotice",
    "FriendAddRequestEvent",
    "GroupJoinRequestEvent",
    "GroupinvItedRequestEvent",
]

