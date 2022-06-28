from typing import TYPE_CHECKING, Any, Dict, NoReturn, Optional, Type

from nonebot.adapters.onebot.exception import ActionFailed as BaseActionFailed

_ERROR_DICT: Dict[str, Type["ActionFailed"]] = {}
# 以retcode为key存到字典里


class ActionFailedMata(type):
    if TYPE_CHECKING:
        status: str
        retcode: int
        message: str
        echo: Optional[str] = None

    def __new__(cls, * args, **kwargs):
        obj: ActionFailed = type.__new__(cls, *args, **kwargs)
        _ERROR_DICT[str(obj.retcode)] = obj
        return obj


class ActionFailed(BaseActionFailed, metaclass=ActionFailedMata):
    status = "failed"
    """执行状态"""
    retcode = -1
    """retcode"""
    message: str
    """错误信息"""
    echo: Optional[str] = None
    """应原样返回动作请求中的 echo"""


class RequestError(ActionFailed):
    """1xxxx 动作请求错误"""
    retcode = 10000


class BadRequestActionFailed(RequestError):
    """10001 无效的动作请求, 格式错误等"""
    retcode = 10001


class UnsupportedActionFailed(RequestError):
    """10002 不支持的动作请求, 不支持的动作"""
    retcode = 10002


class BadParamActionFailed(RequestError):
    """10003 无效的请求参数, 参数缺失或参数类型错误"""
    retcode = 10003


class UnsupportedParamActionFailed(RequestError):
    """10004 不支持的请求参数, 请求参数未实现"""
    retcode = 10004


class UnsupportedSegmentActionFailed(RequestError):
    """10005 不支持的消息段类型, 消息段类型未实现"""
    retcode = 10005


class BadSegmentDataActionFailed(RequestError):
    """10006 无效的消息段数据, 消息段数据格式错误"""
    retcode = 10006


class UnsupportedSegmentDataActionFailed(RequestError):
    """10007 不支持的消息段参数, 消息段参数未实现"""
    retcode = 10007


class HandlerError(ActionFailed):
    """2xxxx 动作处理器错误"""
    retcode = 20000


class BadHandlerActionFailed(HandlerError):
    """20001 动作处理器实现错误, 没有正确设置响应状态等"""
    retcode = 20001


class InternalHandlerErrorActionFailed(HandlerError):
    """20002 动作处理器运行时异常, 未捕获的意料之外的异常"""
    retcode = 20002


# walle_q 扩展
class PrepareFileErrorActionFailed(HandlerError):
    """20003 分片上传文件未prepare, 分片上传文件未prepare"""
    retcode = 20003


# walle_q 扩展
class FileSizeErrorActionFailed(HandlerError):
    """20004 分片上传文件大小错误, 文件大小与预先约定不匹配"""
    retcode = 20004


# walle_q 扩展
class FileSha256ErrorActionFailed(HandlerError):
    """20005 分片上传文件哈希错误, Sha256值与预先约定不匹配"""
    retcode = 20005


class ExecutionError(ActionFailed):
    """3xxxx 动作执行错误"""
    retcode = 30000


class DatabaseError(ExecutionError):
    """31xxx 动作执行错误"""
    retcode = 31000


class FilesystemError(ExecutionError):
    """32xxx 动作执行错误"""
    retcode = 32000


# walle_q 扩展
class FileOpenErrorActionFailed(FilesystemError):
    """32001 文件打开失败, 文件打开失败"""
    retcode = 32001


# walle_q 扩展
class FileReadErrorActionFailed(FilesystemError):
    """32002 文件读取失败, 文件读取失败"""
    retcode = 32002


# walle_q 扩展
class FileCreateErrorActionFailed(FilesystemError):
    """32003 文件创建失败, 文件创建失败"""
    retcode = 32003


# walle_q 扩展
class FileWriteErrorActionFailed(FilesystemError):
    """32004 文件写入失败, 文件写入失败"""
    retcode = 32004


# walle_q 扩展
class FileNotFoundErrorActionFailed(FilesystemError):
    """32005 文件不存在, 文件不存在"""
    retcode = 32005


class NetworkError(ExecutionError):
    """33xxx 动作执行错误"""
    retcode = 33000


# walle_q 扩展
class NetDownloadErrorActionFailed(NetworkError):
    """33001 网络下载错误, 网络下载错误"""
    retcode = 33001


class PlatformError(ExecutionError):
    """34xxx 动作执行错误"""
    retcode = 34000


# walle_q 扩展
class RicqErrorricqActionFailed(PlatformError):
    """34001 未处理报错, ricq报错"""
    retcode = 34001


class LogicError(ExecutionError):
    """35xxx 动作执行错误"""
    retcode = 35000


# walle_q 扩展
class MessageNotExistActionFailed(LogicError):
    """35001 消息不存在, 消息不存在"""
    retcode = 35001


# walle_q 扩展
class FriendNotExistActionFailed(LogicError):
    """35002 好友不存在, 好友不存在"""
    retcode = 35002


# walle_q 扩展
class GroupNotExistActionFailed(LogicError):
    """35003 群不存在, 群不存在"""
    retcode = 35003


# walle_q 扩展
class GroupMemberNotExistActionFailed(LogicError):
    """35004 群成员不存在, 群成员不存在"""
    retcode = 35004


class IAmTired(ExecutionError):
    """36xxx 动作执行错误"""
    retcode = 36000

# walle_q 扩展


class ImageError(ActionFailed):
    """4xxxx 图片解析错误错误段"""
    retcode = 40001


class ImageInfoDecodeErrorActionFailed(BaseActionFailed):
    """41001 图片信息解码错误, 图片信息解码错误"""
    retcode = 41001


class ImageUrlErrorActionFailed(BaseActionFailed):
    """41002 图片URL错误, 图片URL不存在或解析错误"""
    retcode = 41002


class ImagePathErrorActionFailed(BaseActionFailed):
    """41003 图片路径错误, 图片路径不存在或解析错误"""
    retcode = 41003


class ImageDataErrorActionFailed(BaseActionFailed):
    """41004 图片内容错误, 图片文件下载或读取失败"""
    retcode = 41004


def raise_action_error(**raise_data: Optional[Dict[str, Any]]) -> NoReturn:
    retcode = str(raise_data["retcode"])

    assert len(retcode) == 5

    for i in [None, -2, -3, -4]:
        rise_error = _ERROR_DICT.get(retcode[:i].ljust(5, "0"))
        if rise_error is not None:
            raise rise_error(**raise_data)

    raise ActionFailed(**raise_data)
