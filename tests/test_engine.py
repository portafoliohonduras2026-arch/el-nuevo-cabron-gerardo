import asyncio
import pytest
from core.engine import Engine

@pytest.mark.asyncio
async def test_engine_isolates_crash_and_continues():
    processed = []
    async def handler(payload):
        if payload.get("boom"):
            raise RuntimeError("Fallo simulado")
        processed.append(payload)

    engine = Engine(handler=handler, max_queue_size=10)
    task = asyncio.create_task(engine.run())
    await engine.submit({"boom": True})
    await engine.submit({"ok": 1})
    await asyncio.sleep(0.05)
    await engine.stop()
    await task
    assert processed == [{"ok": 1}]
