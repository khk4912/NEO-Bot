from typing import Union
import aiohttp
from utils.exceptions import NotAllowedStatusException


class HTTP:
    @staticmethod
    async def get(
        url: str,
        params: dict = None,
        json: bool = False,
        status: int = None,
        **kwargs,
    ) -> Union[str, dict]:
        async with aiohttp.ClientSession(**kwargs) as session:
            async with session.get(url, params=params) as r:
                if status is not None:
                    if r.status != status:
                        raise NotAllowedStatusException(r.status)
                if json:
                    return await r.json()
                return await r.text()

    @staticmethod
    async def post(
        url: str,
        data: dict,
        params: dict = None,
        json: bool = False,
        status: int = None,
        **kwargs,
    ) -> Union[str, dict]:
        async with aiohttp.ClientSession(**kwargs) as session:
            async with session.post(url, data=data, params=params) as r:
                if status is not None:
                    if r.status != status:
                        raise NotAllowedStatusException(r.status)
                if json:
                    return await r.json()
                return await r.text()
