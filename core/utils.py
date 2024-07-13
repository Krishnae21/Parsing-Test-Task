import functools
import httpx
from typing import Any, Callable

from loguru import logger


def handle_http_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPStatusError as exc:
            logger.warning(f"HTTP error occurred: {exc}")
            raise exc
        except httpx.RequestError as exc:
            logger.warning(f"An error occurred while requesting {exc}.")
            raise exc
        except Exception as exc:
            logger.warning(f"An unexpected error occurred: {exc}")
            raise exc

    return wrapper
