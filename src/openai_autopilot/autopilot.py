from typing import Coroutine
import os
import asyncio
from openai import AsyncOpenAI
from tqdm import tqdm
import random
import json


class AlreadyProcessedException(Exception):
    """Exception raised when data has already been processed."""

    def __init__(self, message="Data has already been processed"):
        self.message = message
        super().__init__(self.message)


class InvalidOutputTypeError(Exception):
    """Exception raised when output text is not a string."""

    def __init__(self, output):
        self.output = output
        self.message = (
            f"Expected string type for output, got {type(output).__name__} instead."
        )
        super().__init__(self.message)


class Autopilot:
    def __init__(
        self,
        client: AsyncOpenAI = None,
        process_fn: Coroutine = None,
        concurrency: int = 5,
        tmp_dir: str = "tmp",
        tmp_file_prefix: str = "data",
        verbose: bool = False,
    ):
        self._client = client
        self._process_fn = process_fn
        self._concurrency = concurrency
        self._data_queue = asyncio.Queue()
        self._pbar = None
        self._tmp_dir = tmp_dir
        self._tmp_file_prefix = tmp_file_prefix
        self._verbose = verbose

    # check queue format
    def validate(self):
        pass

    async def _worker(self, worker_id: int):
        while not self._data_queue.empty():
            # fetch data from queue
            data_id, messages = await self._data_queue.get()
            try:
                if self._verbose:
                    print(f"worker {worker_id}: working on {data_id}")

                tmp_file = os.path.join(
                    self._tmp_dir, f"{self._tmp_file_prefix}_{data_id}.txt"
                )

                # skip data processing if temp file exists
                if os.path.isfile(tmp_file):
                    raise AlreadyProcessedException(
                        f"Data with idx {data_id} has already been processed."
                    )

                # run process function
                response_text = await self._process_fn(
                    worker_id, self._client, data_id, messages
                )

                # write temp file
                if not isinstance(response_text, str):
                    raise InvalidOutputTypeError(response_text)

                with open(tmp_file, "w", encoding="utf8") as f:
                    f.write(response_text)

            except AlreadyProcessedException:
                if self._verbose:
                    print(f"worker {worker_id}: skipping on {data_id}")

            except InvalidOutputTypeError:
                if self._verbose:
                    print(
                        f"worker {worker_id}: process function return non string type, {type(response_text).__name__}"
                    )
                    print(f"worker {worker_id}: exiting")
                    break

            except Exception as e:
                print(e)

            finally:
                self._pbar.update(1)

    async def _run(self):
        # create tmp folder
        os.makedirs(self._tmp_dir, exist_ok=True)
        self._pbar = tqdm(total=self._data_queue.qsize(), desc="Progress")

        # create workers
        tasks = [
            asyncio.create_task(self._worker(worker_id))
            for worker_id in range(self._concurrency)
        ]

        # run until worker fetched all data in the queue
        await asyncio.gather(*tasks)

    def _post_process(self, data_list):
        for i, data in enumerate(data_list):
            data_id = data["id"]

            try:
                tmp_file = os.path.join(
                    self._tmp_dir, f"{self._tmp_file_prefix}_{data_id}.txt"
                )

                # file response with empty string if tmp file does not exist
                if not os.path.isfile(tmp_file):
                    data_list[i]["response"] = ""
                    continue

                # read response back from tmp file
                with open(tmp_file, "r", encoding="utf8") as f:
                    data_list[i]["response"] = f.read()

            except Exception as e:
                print(e)

        return data_list

    def run(self, data_list: list[dict[str, int | list[dict[str, str]]]]):
        # add data to queue
        for data in data_list:
            data_id, messages = data["id"], data["messages"]
            self._data_queue.put_nowait((data_id, messages))

        # run process function parallelly
        asyncio.run(self._run())

        # map response text input original data list
        data_list = self._post_process(data_list)
        return data_list


if __name__ == "__main__":

    async def mock_fn(worker_id, client, idx, messages):
        await asyncio.sleep(random.randint(1, 20) / 10)

        return f"test {idx}"

    autopilot = Autopilot(process_fn=mock_fn, verbose=True)

    # data_list -> data[]
    # data -> dict[id, message, response]

    data_list = autopilot.run(
        [
            {"id": i, "messages": [{"role": "system", "content": "system prompt"}]}
            for i in range(30)
        ]
    )
    print(json.dumps(data_list, indent=2))
