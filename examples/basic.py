from typing import Coroutine
import asyncio
import random
import json
from openai import AsyncOpenAI
from openai_autopilot import Autopilot, AutopilotMessageType


async def process(
    worker_id: int, client: AsyncOpenAI, idx: int, messages: AutopilotMessageType
) -> Coroutine[None, None, str]:
    await asyncio.sleep(random.randint(1, 20) / 10)
    return f"test {idx}"


autopilot = Autopilot(process_fn=process, verbose=True)

data_list = autopilot.run(
    [
        {"id": i, "messages": [{"role": "system", "content": "system prompt"}]}
        for i in range(30)
    ]
)
print(json.dumps(data_list, indent=2))
