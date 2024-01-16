from typing import Coroutine, List
import asyncio
import random
from openai import AsyncOpenAI
from openai_autopilot import Autopilot, AutopilotMessage, AutopilotDataList


async def process(
    worker_id: int, client: AsyncOpenAI, data_id: int, messages: List[AutopilotMessage]
) -> Coroutine[None, None, str]:
    await asyncio.sleep(random.randint(1, 20) / 10)
    return f"process {data_id} by worker {worker_id}"


autopilot = Autopilot(client=None, process_fn=process, verbose=True)

data_list = autopilot.run(
    AutopilotDataList(
        data_list=[
            {"id": i, "messages": [{"role": "system", "content": "system prompt"}]}
            for i in range(30)
        ]
    )
)

print("output")
print(data_list.model_dump_json(indent=2))
