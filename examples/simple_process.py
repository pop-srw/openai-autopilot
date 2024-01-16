from typing import Coroutine, List
import os
from openai import AsyncOpenAI
from openai_autopilot import Autopilot, AutopilotMessage, AutopilotDataList


async def process(
    worker_id: int, client: AsyncOpenAI, data_id: int, messages: List[AutopilotMessage]
) -> Coroutine[None, None, str]:
    chat_completion = await client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    completion_text = chat_completion.choices[0].message.content
    return completion_text


api_key = os.environ.get("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key, max_retries=3)
autopilot = Autopilot(client=client, process_fn=process)

food_names = ["pizza", "burger", "ramen"]
data_list = autopilot.run(
    AutopilotDataList(
        data_list=[
            {
                "id": i,
                "messages": [
                    {
                        "role": "system",
                        "content": "You're a Sous Chef. Please response a recipe of a given food name.",
                    },
                    {"role": "user", "content": food_name},
                ],
            }
            for i, food_name in enumerate(food_names)
        ]
    )
)

print("output")
print(data_list.model_dump_json(indent=2))
