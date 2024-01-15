import pytest

from openai_autopilot.autopilot import Autopilot
from openai_autopilot.types import AutopilotMessageType


def test_valid_format_not_return_error(mocker):
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

    try:
        autopilot.run(
            [
                {
                    "id": 0,
                    "messages": [{"role": "system", "content": "system prompt"}],
                }
            ]
        )
    except Exception:
        pytest.fail("unexpected error")


def test_invalid_id_key_return_error(mocker):
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

    with pytest.raises(KeyError):
        autopilot.run(
            [
                {
                    "id_xxx": 0,
                    "messages": [{"role": "system", "content": "system prompt"}],
                }
            ]
        )


def test_invalid_messages_key_return_error(mocker):
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

    with pytest.raises(KeyError):
        autopilot.run(
            [
                {
                    "id": 0,
                    "messages_xxx": [{"role": "system", "content": "system prompt"}],
                }
            ]
        )


def test_invalid_message_role_key_return_error(mocker):
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

    with pytest.raises(KeyError):
        autopilot.run(
            [
                {
                    "id": 0,
                    "messages": [{"role_xxx": "system", "content": "system prompt"}],
                }
            ]
        )


def test_invalid_message_content_key_return_error(mocker):
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

    with pytest.raises(KeyError):
        autopilot.run(
            [
                {
                    "id": 0,
                    "messages": [{"role": "system", "content_xxx": "system prompt"}],
                }
            ]
        )
