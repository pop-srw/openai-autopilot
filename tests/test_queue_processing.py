import pytest

from openai_autopilot.autopilot import Autopilot
from openai_autopilot.types import AutopilotMessageType


def test_queue_processing(mocker):
    # disable data processing
    mocker.patch.object(Autopilot, "_run")
    mocker.patch.object(Autopilot, "_post_process")

    async def mock_process_fn(worker_id, client, idx, messages):
        return "processed response"

    # initialize Autopilot with the mocked process function
    autopilot = Autopilot(
        client=None,
        process_fn=mock_process_fn,
        concurrency=1,
    )

    autopilot.run(
        [
            {"id": i, "messages": [{"role": "system", "content": "system prompt"}]}
            for i in range(3)
        ]
    )

    assert autopilot._data_queue.qsize() == 3

    # Initialize Autopilot with the mocked process function
    autopilot = Autopilot(
        client=None,
        process_fn=mock_process_fn,
        concurrency=1,
    )

    autopilot.run(
        [
            {"id": i, "messages": [{"role": "system", "content": "system prompt"}]}
            for i in range(30)
        ]
    )

    assert autopilot._data_queue.qsize() == 30

    # Initialize Autopilot with the mocked process function
    autopilot = Autopilot(
        client=None,
        process_fn=mock_process_fn,
        concurrency=1,
    )

    autopilot.run(
        [
            {"id": i, "messages": [{"role": "system", "content": "system prompt"}]}
            for i in range(0)
        ]
    )

    assert autopilot._data_queue.qsize() == 0
