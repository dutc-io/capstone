from inspect import signature
from logging import DEBUG, basicConfig, getLogger
from contextlib import asynccontextmanager
from collections import namedtuple
from dataclasses import dataclass

from httpx import AsyncClient, Timeout

logger = getLogger(__name__)
basicConfig(
    level=DEBUG,
    format="%(asctime)s %(levelname)s %(name)-10s %(message)s",
    datefmt="%d-%b %H:%M:%S",
)

TIMEOUTS = Timeout(5.0, read=5.0, write=5.0, connect=5.0, pool=5.0)
CASINO = "http://127.0.0.1:8000/v1/"


class Endpoints:
    REGISTRY = {}

    @classmethod
    def register(cls, ep):
        def dec(f):
            cls.REGISTRY[ep] = f.__name__
            return f

        return dec


@dataclass
class Casino:

    client: AsyncClient
    API: str

    async def get(self, endpoint):
        return (await self.client.get(f"{self.API}{endpoint}")).json()

    async def post(self, endpoint, params):
        try:
            return (await self.client.post(f"{self.API}{endpoint}", json=params)).json()
        except Exception as e:
            print(e)

    @Endpoints.register("discard")
    async def discard(self, *, params: dict):
        """"""
        return await self.post("discard/", params)

    @Endpoints.register("build")
    async def build(self, *, params: dict):
        """"""
        return await self.post("build/", params)

    @Endpoints.register("capture")
    async def capture(self, *, params: dict):
        """"""
        return await self.post("capture/", params)

    @Endpoints.register("create")
    async def create(self, *, params: dict):
        """Create a new game"""
        return await self.post("create/", params)

    @Endpoints.register("save")
    async def save(self, *, params: dict):
        """"""
        return await self.post("save/", params)

    @Endpoints.register("state")
    async def state(self):
        """"""
        return await self.get("state/")

    @Endpoints.register("test")
    async def test(self):
        """POL"""
        return await self.get("test/simple/")

    @classmethod
    @asynccontextmanager
    async def connect(cls, *, API=CASINO):

        headers = {
            "User-Agent": "Barriere d'Enghien-les-Bains",
            "Content-Type": "application/json",
        }
        async with AsyncClient(
            headers=headers, http2=True, follow_redirects=True
        ) as client:
            yield cls(client, API=API)


ENDPOINTS = Endpoints.REGISTRY
