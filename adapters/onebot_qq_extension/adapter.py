import json
from typing import Any

from nonebot.adapters import Bot
from nonebot.adapters.onebot.collator import Collator
from nonebot.adapters.onebot.exception import ApiNotAvailable, NetworkError
from nonebot.adapters.onebot.utils import CustomEncoder
from nonebot.adapters.onebot.v12 import Adapter as BaseAdapter
from nonebot.adapters.onebot.v12 import log
from nonebot.adapters.onebot.v12.adapter import COLLATOR_KEY, DEFAULT_MODELS
from nonebot.drivers import ForwardDriver, Request
from nonebot.typing import overrides
from pygtrie import StringTrie

from .utils import handle_api_result


class Adapter(BaseAdapter):
    name = "OneBot V12 QQ Extension Adapter"

    event_models: StringTrie = StringTrie(separator="/")
    event_models[""] = Collator(
        name,
        DEFAULT_MODELS,
        COLLATOR_KEY,
    )

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return cls.name

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        websocket = self.connections.get(bot.self_id, None)
        timeout: float = data.get("_timeout", self.config.api_timeout)
        log("DEBUG", f"Calling API <y>{api}</y>")

        if websocket:
            seq = self._result_store.get_seq()
            json_data = json.dumps(
                {"action": api, "params": data, "echo": str(seq)},
                cls=CustomEncoder,
            )
            await websocket.send(json_data)
            return handle_api_result(
                await self._result_store.fetch(bot.self_id, seq, timeout)
            )

        elif isinstance(self.driver, ForwardDriver):
            api_url = self.onebot_config.onebot_api_roots.get(bot.self_id)
            if not api_url:
                raise ApiNotAvailable

            headers = {"Content-Type": "application/json"}
            if self.onebot_config.onebot_access_token is not None:
                headers["Authorization"] = (
                    "Bearer " + self.onebot_config.onebot_access_token
                )

            request = Request(
                "POST",
                api_url,
                headers=headers,
                timeout=timeout,
                content=json.dumps(
                    {"action": api, "params": data}, cls=CustomEncoder),
            )

            try:
                response = await self.driver.request(request)

                if 200 <= response.status_code < 300:
                    if not response.content:
                        raise ValueError("Empty response")
                    result = json.loads(response.content)
                    return handle_api_result(result)
                raise NetworkError(
                    f"HTTP request received unexpected "
                    f"status code: {response.status_code}"
                )
            except NetworkError:
                raise
            except Exception as e:
                raise NetworkError("HTTP request failed") from e
        else:
            raise ApiNotAvailable
