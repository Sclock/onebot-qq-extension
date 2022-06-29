from typing import TYPE_CHECKING, Any, Dict, NoReturn, Optional, Type
from .exception import raise_action_error


def handle_api_result(result: Optional[Dict[str, Any]]) -> Any:
    """处理 API 请求返回值。

    参数:
        result: API 返回数据

    返回:
        API 调用返回数据

    异常:
        ActionFailed: API 调用失败
    """
    if isinstance(result, dict):
        print(result)
        if result.get("status") == "failed":
            raise_action_error(**result)
        return result.get("data")
