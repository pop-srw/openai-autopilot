from typing import Coroutine
import asyncio
import random
import json
from openai import AsyncOpenAI
from openai_autopilot import Autopilot, AutopilotMessageType


async def process(
    worker_id: int, client: AsyncOpenAI, data_id: int, messages: AutopilotMessageType
) -> Coroutine[None, None, str]:
    await asyncio.sleep(random.randint(1, 20) / 10)

    return f"process {data_id} by worker {worker_id}"


autopilot = Autopilot(client=None, process_fn=process, verbose=True)

data_list = autopilot.run(
    [
        {"id": i, "messages": [{"role": "system", "content": "system prompt"}]}
        for i in range(30)
    ]
)

print("output")
print(json.dumps(data_list, indent=2))
