from nonebot.adapters.onebot.exception import ActionFailed as BaseActionFailed
from typing import Optional, Literal
# from pydantic.main import BaseModel


class ActionFailed(BaseActionFailed):
    status: Literal["failed"]
    retcode: int
    message: str
    echo: Optional[str] = None


class RequestError(ActionFailed):
    """1xxxx 动作请求错误"""
    pass


class BadRequestActionFailed(RequestError):
    """10001 无效的动作请求, 格式错误等"""
    # msg: Literal["friend"]
    pass


class UnsupportedActionFailed(RequestError):
    """10002 不支持的动作请求, 不支持的动作"""
    pass


class BadParamActionFailed(RequestError):
    """10003 无效的请求参数, 参数缺失或参数类型错误"""
    pass


class UnsupportedParamActionFailed(RequestError):
    """10004 不支持的请求参数, 请求参数未实现"""
    pass


class UnsupportedSegmentActionFailed(RequestError):
    """10005 不支持的消息段类型, 消息段类型未实现"""
    pass


class BadSegmentDataActionFailed(RequestError):
    """10006 无效的消息段数据, 消息段数据格式错误"""
    pass


class UnsupportedSegmentDataActionFailed(RequestError):
    """10007 不支持的消息段参数, 消息段参数未实现"""
    pass


class HandlerError(ActionFailed):
    """2xxxx 动作处理器错误"""
    pass


class BadHandlerActionFailed(HandlerError):
    """20001 动作处理器实现错误, 没有正确设置响应状态等"""
    pass


class InternalHandlerErrorActionFailed(HandlerError):
    """20002 动作处理器运行时异常, 未捕获的意料之外的异常"""
    pass


class PrepareFileErrorActionFailed(HandlerError):
    """20003 分片上传文件未prepare, 分片上传文件未prepare"""
    pass


class FileSizeErrorActionFailed(HandlerError):
    """20004 分片上传文件大小错误, 文件大小与预先约定不匹配"""
    pass


class FileSha256ErrorActionFailed(HandlerError):
    """20005 分片上传文件哈希错误, Sha256值与预先约定不匹配"""
    pass


class ExecutionError(ActionFailed):
    """3xxxx 动作执行错误"""
    pass


class FileOpenErrorActionFailed(ExecutionError):
    """32001 文件打开失败, 文件打开失败"""
    pass


class FileReadErrorActionFailed(ExecutionError):
    """32002 文件读取失败, 文件读取失败"""
    pass


class FileCreateErrorActionFailed(ExecutionError):
    """32003 文件创建失败, 文件创建失败"""
    pass


class FileWriteErrorActionFailed(ExecutionError):
    """32004 文件写入失败, 文件写入失败"""
    pass


class FileNotFoundErrorActionFailed(ExecutionError):
    """32005 文件不存在, 文件不存在"""
    pass


class NetDownloadErrorActionFailed(ExecutionError):
    """33001 网络下载错误, 网络下载错误"""
    pass


class RicqErrorricqActionFailed(ExecutionError):
    """34001 未处理报错, ricq报错"""
    pass


class MessageNotExistActionFailed(ExecutionError):
    """35001 消息不存在, 消息不存在"""
    pass


class FriendNotExistActionFailed(ExecutionError):
    """35002 好友不存在, 好友不存在"""
    pass


class GroupNotExistActionFailed(ExecutionError):
    """35003 群不存在, 群不存在"""
    pass


class GroupMemberNotExistActionFailed(ExecutionError):
    """35004 群成员不存在, 群成员不存在"""
    pass


class ImageError(ActionFailed):
    """4xxxx 图片解析错误错误段"""
    pass


class ImageInfoDecodeErrorActionFailed(BaseActionFailed):
    """41001 图片信息解码错误, 图片信息解码错误"""
    pass


class ImageUrlErrorActionFailed(BaseActionFailed):
    """41002 图片URL错误, 图片URL不存在或解析错误"""
    pass


class ImagePathErrorActionFailed(BaseActionFailed):
    """41003 图片路径错误, 图片路径不存在或解析错误"""
    pass


class ImageDataErrorActionFailed(BaseActionFailed):
    """41004 图片内容错误, 图片文件下载或读取失败"""
    pass


class OutherError(ActionFailed):
    """其它错误段"""
    pass
