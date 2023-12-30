from typing import Coroutine
import asyncio
from openai import AsyncOpenAI
from tqdm import tqdm
import random


class Autopilot:
    def __init__(
        self,
        client: AsyncOpenAI = None,
        process_fn: Coroutine = None,
        concurrency: int = 5,
    ):
        self._client = client
        self._process_fn = process_fn
        self._concurrency = concurrency
        self._data_queue = asyncio.Queue()
        self._pbar = None

    def add_data(self, idx: int, messages: list[dict[str, str]]):
        self._data_queue.put_nowait((idx, messages))

    # check queue format
    def validate(self):
        pass

    # workers fetch queue -> check tmp file -> process() -> update pbar -> save tmp file idx
    async def _worker(self, worker_id: int):
        while not self._data_queue.empty():
            idx, messages = await self._data_queue.get()
            try:
                await self._process_fn(worker_id, self._client, idx, messages)
            except Exception as e:
                print("error:")
                print(e)
            finally:
                self._pbar.update(1)

    async def _run(self):
        self._pbar = tqdm(total=self._data_queue.qsize(), desc="Progress")

        tasks = [
            asyncio.create_task(self._worker(worker_id))
            for worker_id in range(self._concurrency)
        ]
        await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self._run())


if __name__ == "__main__":
    print("ok")

    async def mock_fn(worker_id, client, idx, messages):
        print(f"worker {worker_id}: work on {idx}")
        await asyncio.sleep(random.randint(1, 20) / 10)

    autopilot = Autopilot(process_fn=mock_fn)
    x = [autopilot.add_data(i, []) for i in range(1000)]

    # asyncio.run(autopilot.run())
    autopilot.run()
