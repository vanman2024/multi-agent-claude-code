from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI, Request


def create_callback_app(store: List[Dict[str, Any]] | None = None) -> FastAPI:
    """Create a tiny FastAPI app for testing callback/webhook flows.

    Collected payloads are appended to the provided store list.
    """
    app = FastAPI()
    payloads: List[Dict[str, Any]] = store if store is not None else []

    @app.post("/webhook")
    async def webhook(req: Request):
        data = await req.json()
        payloads.append(data)
        return {"ok": True}

    @app.get("/payloads")
    async def get_payloads():
        return payloads

    return app

