from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Receive, Send


class ASGIAuthenticationMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)

        await self.app(scope, receive, send)
