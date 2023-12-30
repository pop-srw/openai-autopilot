import asyncio
import random
import json
from openai_autopilot import Autopilot


if __name__ == "__main__":

    async def process(worker_id, client, idx, messages):
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
