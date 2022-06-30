import asyncio
import contextlib
import json
from typing import Any, Optional, cast

import msgpack
from nonebot.adapters.onebot.collator import Collator
from nonebot.adapters.onebot.exception import ApiNotAvailable, NetworkError
from nonebot.adapters.onebot.utils import CustomEncoder
from nonebot.adapters.onebot.v12 import Adapter as BaseAdapter
from nonebot.adapters.onebot.v12.adapter import COLLATOR_KEY, DEFAULT_MODELS, RECONNECT_INTERVAL
from nonebot.drivers import URL, ForwardDriver, Request, Response, WebSocket
from nonebot.exception import WebSocketClosed
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from pygtrie import StringTrie

from .bot import Bot
from .log import log
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

    async def _handle_ws(self, websocket: WebSocket) -> None:
        self_id = websocket.request.headers.get("X-Self-Id")

        # check self_id
        if not self_id:
            log("WARNING", "Missing X-Self-ID Header")
            await websocket.close(1008, "Missing X-Self-ID Header")
            return
        elif self_id in self.bots:
            log("WARNING", f"There's already a bot {self_id}, ignored")
            await websocket.close(1008, "Duplicate X-Self-ID")
            return

        # check access_token
        response = self._check_access_token(websocket.request)
        if response is not None:
            content = cast(str, response.content)
            await websocket.close(1008, content)
            return

        await websocket.accept()
        bot = Bot(self, self_id)
        self.connections[self_id] = websocket
        self.bot_connect(bot)

        log("INFO", f"<y>Bot {escape_tag(self_id)}</y> connected")

        try:
            while True:
                data = await websocket.receive()
                raw_data = (
                    json.loads(data) if isinstance(
                        data, str) else msgpack.unpackb(data)
                )
                event = self.json_to_event(raw_data, self_id)
                if event:
                    asyncio.create_task(bot.handle_event(event))
        except WebSocketClosed as e:
            log("WARNING",
                f"WebSocket for Bot {escape_tag(self_id)} closed by peer")
        except Exception as e:
            log(
                "ERROR",
                f"<r><bg #f8bbd0>Error while process data from websocketfor bot {escape_tag(self_id)}.</bg #f8bbd0></r>",
                e,
            )

        finally:
            with contextlib.suppress(Exception):
                await websocket.close()
            self.connections.pop(self_id, None)
            self.bot_disconnect(bot)

    async def _handle_http(self, request: Request) -> Response:
        self_id = request.headers.get("x-self-id")

        # check self_id
        if not self_id:
            log("WARNING", "Missing X-Self-ID Header")
            return Response(400, content="Missing X-Self-ID Header")

        # check access_token
        response = self._check_access_token(request)
        if response is not None:
            return response

        data = request.content
        if data is not None:
            json_data = json.loads(data)
            event = self.json_to_event(json_data)
            if event:
                bot = self.bots.get(self_id, None)
                if not bot:
                    bot = Bot(self, self_id)
                    self.bot_connect(bot)
                    log("INFO", f"<y>Bot {escape_tag(self_id)}</y> connected")
                bot = cast(Bot, bot)
                asyncio.create_task(bot.handle_event(event))
        return Response(204)

    async def _forward_ws(self, url: URL) -> None:
        headers = {}
        if self.onebot_config.onebot_access_token:
            headers[
                "Authorization"
            ] = f"Bearer {self.onebot_config.onebot_access_token}"
        req = Request("GET", url, headers=headers, timeout=30.0)
        bot: Optional[Bot] = None
        while True:
            try:
                async with self.websocket(req) as ws:
                    log(
                        "DEBUG",
                        f"WebSocket Connection to {escape_tag(str(url))} established",
                    )
                    try:
                        while True:
                            data = await ws.receive()
                            raw_data = (
                                json.loads(data)
                                if isinstance(data, str)
                                else msgpack.unpackb(data)
                            )
                            event = self.json_to_event(
                                raw_data, bot and bot.self_id)
                            if not event:
                                continue
                            if not bot:
                                self_id = event.self_id
                                bot = Bot(self, self_id)
                                self.connections[self_id] = ws
                                self.bot_connect(bot)
                                log(
                                    "INFO",
                                    f"<y>Bot {escape_tag(str(self_id))}</y> connected",
                                )
                            asyncio.create_task(bot.handle_event(event))
                    except WebSocketClosed as e:
                        log(
                            "ERROR",
                            "<r><bg #f8bbd0>WebSocket Closed</bg #f8bbd0></r>",
                            e,
                        )
                    except Exception as e:
                        log(
                            "ERROR",
                            "<r><bg #f8bbd0>Error while process data from websocket"
                            f"{escape_tag(str(url))}. Trying to reconnect...</bg #f8bbd0></r>",
                            e,
                        )
                    finally:
                        if bot:
                            self.connections.pop(bot.self_id, None)
                            self.bot_disconnect(bot)
                            bot = None

            except Exception as e:
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Error while setup websocket to "
                    f"{escape_tag(str(url))}. Trying to reconnect...</bg #f8bbd0></r>",
                    e,
                )

            await asyncio.sleep(RECONNECT_INTERVAL)
