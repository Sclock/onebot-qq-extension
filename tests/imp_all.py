from pathlib import Path

import nonebot.adapters
nonebot.adapters.__path__.append(  # type: ignore
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)

from nonebot.adapters.onebot_qq_extension.exception import *