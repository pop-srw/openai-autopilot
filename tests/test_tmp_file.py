# def test_xx(mocker):
#     mocker.patch("os.makedirs")
#     mocker.patch("os.path.isfile")

#     # Initialize Autopilot with the mocked process function
#     autopilot = Autopilot(
#         client=None,  # Mock or replace with a suitable object
#         process_fn=mock_process_fn,
#         concurrency=1,
#         tmp_dir="tmp",  # Specify a test directory
#         tmp_file_prefix="test_data",
#         verbose=True,
#     )

#     test_data_id = 71
#     test_messages: AutopilotMessageType = [
#         {"role": "system", "content": "system prompt"}
#     ]

#     autopilot.run([{"id": test_data_id, "messages": test_messages}])

#     # os.makedirs.assert_called_once_with("file")

#     # Assertions to verify the behavior
#     os.makedirs.assert_called_once_with(autopilot._tmp_dir, exist_ok=True)

#     os.path.isfile.assert_called_with("tmp/test_data_71.txt", "w", encoding="utf8")
#     mock_isfile.assert_called_with("tmp/test_data_71.txt")
