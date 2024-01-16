import pytest
from openai_autopilot.autopilot import Autopilot
from openai_autopilot.types import AutopilotDataList


def test_tmp_folder_created(mocker):
    makedirs_mock = mocker.patch("os.makedirs")

    async def mock_process_fn(worker_id, client, idx, messages):
        return ""

    autopilot = Autopilot(
        client=None,
        process_fn=mock_process_fn,
        concurrency=1,
        tmp_dir="fake_tmp_dir",
        tmp_file_prefix="test_data",
        verbose=True,
    )

    autopilot.run(
        AutopilotDataList(
            data_list=[
                {"id": 11, "messages": [{"role": "system", "content": "system prompt"}]}
            ]
        )
    )

    makedirs_mock.assert_called_once_with("fake_tmp_dir", exist_ok=True)


def test_write_file_if_tmp_file_not_exists(mocker):
    mocker.patch("os.makedirs")
    mocker.patch("os.path.isfile", side_effect=[False, True])
    open_mock = mocker.patch("builtins.open", mocker.mock_open())

    async def mock_process_fn(worker_id, client, idx, messages):
        return "fake response"

    autopilot = Autopilot(
        client=None,
        process_fn=mock_process_fn,
        concurrency=1,
        tmp_dir="tmp",
        tmp_file_prefix="test_data",
        verbose=True,
    )

    autopilot.run(
        AutopilotDataList(
            data_list=[
                {"id": 21, "messages": [{"role": "system", "content": "system prompt"}]}
            ]
        )
    )

    # check tmp file is open for writing
    assert (
        mocker.call("tmp/test_data_21.txt", "w", encoding="utf8")
        in open_mock.mock_calls
    )

    # check tmp file is written with fake response
    open_mock().write.assert_called_once_with("fake response")


def test_skip_processing_if_tmp_file_exists(mocker):
    mocker.patch("os.makedirs")
    mocker.patch("os.path.isfile", side_effect=[True, True])
    open_mock = mocker.patch("builtins.open", mocker.mock_open())

    async def mock_process_fn(worker_id, client, idx, messages):
        return "fake response"

    autopilot = Autopilot(
        client=None,
        process_fn=mock_process_fn,
        concurrency=1,
        tmp_dir="tmp",
        tmp_file_prefix="test_data",
        verbose=True,
    )

    autopilot.run(
        AutopilotDataList(
            data_list=[
                {"id": 31, "messages": [{"role": "system", "content": "system prompt"}]}
            ]
        )
    )

    # check tmp file is not open for writing
    assert (
        mocker.call("tmp/test_data_31.txt", "w", encoding="utf8")
        not in open_mock.mock_calls
    )


def test_read_file_is_read_in_post_process(mocker):
    mocker.patch("os.makedirs")
    mocker.patch("os.path.isfile", side_effect=[False, True])
    open_mock = mocker.patch(
        "builtins.open", mocker.mock_open(read_data="fake response")
    )

    async def mock_process_fn(worker_id, client, idx, messages):
        return ""

    autopilot = Autopilot(
        client=None,
        process_fn=mock_process_fn,
        concurrency=1,
        tmp_dir="tmp",
        tmp_file_prefix="test_data",
        verbose=True,
    )

    data_list = autopilot.run(
        AutopilotDataList(
            data_list=[
                {"id": 41, "messages": [{"role": "system", "content": "system prompt"}]}
            ]
        )
    )

    # check tmp file is not open for reading
    assert (
        mocker.call("tmp/test_data_41.txt", "r", encoding="utf8")
        in open_mock.mock_calls
    )

    # check file is read
    open_mock().read.assert_called_once()

    # check response is added to output data list
    assert data_list.data_list[0].response == "fake response"
