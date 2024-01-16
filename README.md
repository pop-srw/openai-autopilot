<p align="center">
    <img src="https://raw.githubusercontent.com/pop-srw/openai-autopilot/main/docs/logo.png" alt="Autopilot logo" width="150" />
    <h1 align="center">OpenAI Autopilot</h1>
</p>

[![PyPI - Version](https://img.shields.io/pypi/v/openai-autopilot.svg)](https://pypi.org/project/openai-autopilot)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openai-autopilot.svg)](https://pypi.org/project/openai-autopilot)

Autopilot simplifies your OpenAI interactions by concurrently processing multiple tasks, significantly speeding up data handling. It uses temporary files for checkpointing, ensuring no progress is lost during unexpected interruptions. Plus, with its real-time progress tracking, you're always informed about your task completion status, making your workflow not only faster but also more reliable and transparent.

---

**Table of Contents**

- [Features](#features)
- [How it works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration Options](#configuration-options)
- [Example](#example)
- [License](#license)

## Features

- **Concurrent Processing**: Efficiently handles multiple OpenAI tasks in parallel, greatly speeding up data processing.
- **Checkpointing with Temporary Files**: Safely saves progress using temporary files, allowing continuation from the last checkpoint in case of interruptions.
- **Real-Time Progress Tracking**: Features a progress bar that provides immediate updates on the status of ongoing tasks, enhancing transparency and planning.
- **Asynchronous Operation**: Leverages Python's asyncio for non-blocking task execution, improving overall performance.
- **Error Handling**: Robust exception management to ensure smooth operation under various scenarios.
- **Type Checking with Pydantic**: Utilizes Pydantic for rigorous data validation and type checking, ensuring that the inputs and outputs of tasks adhere to defined schemas. This enhances the reliability and consistency of the data being processed.

## How it works

The Autopilot framework streamlines asynchronous data processing with OpenAI's API. It queues data items and processes them using multiple concurrent workers, each executing a user-defined function that interacts with the OpenAI API. Importantly, if a temporary file for a task already exists, Autopilot skips reprocessing it, efficiently avoiding redundant work. As tasks are completed, results are saved in temporary files, allowing the process to resume seamlessly from the last checkpoint in case of interruptions. This setup ensures efficient handling and error management. Progress is visually tracked, and upon completion, results are compiled into a structured format for final use, simplifying the complexity of asynchronous operations.

## Installation

```shell
pip install openai-autopilot
```

## Usage

In this section, we demonstrate how to utilize the Autopilot for efficient asynchronous data processing with OpenAI's API. The process involves defining a custom asynchronous function that interfaces with OpenAI, initializing the OpenAI client, setting up the Autopilot with the processing function, and executing the process with your data. The steps are as follows:

1. **Define the Processing Function**: Create an `async` function named `process`, which encapsulates the logic for interacting with OpenAI's API.

2. **Initialize OpenAI Client**: Set up the `AsyncOpenAI` client using your OpenAI API key.

3. **Configure Autopilot**: Instantiate the `Autopilot` class with the initialized OpenAI client and the custom processing function.

4. **Run the Process**: Use the `run` method of the Autopilot instance, passing in your data encapsulated in `AutopilotDataList`.

5. **Access Processed Data**: The `run` method returns the processed data, which can be used as needed.

This setup is designed to offer a straightforward approach to handling asynchronous tasks with OpenAI, enhancing both efficiency and ease of use.

```python
from typing import Coroutine, List
from openai import AsyncOpenAI
from openai_autopilot import Autopilot, AutopilotMessage, AutopilotDataList

# Define the processing function, wrapping around the normal OpenAI async API usage
async def process(
    worker_id: int, client: AsyncOpenAI, data_id: int, messages: List[AutopilotMessage]
) -> Coroutine[None, None, str]:
    chat_completion = await client.chat.completions.create(
        # ...insert your configuration here...
    )

    completion_text = chat_completion.choices[0].message.content

    # Return the string to be added to the response of your data
    return completion_text

# Initialize the OpenAI asynchronous client
api_key = "...your api key..."
client = AsyncOpenAI(api_key=api_key)
autopilot = Autopilot(client=client, process_fn=process)

processed_data = autopilot.run(
    AutopilotDataList(
        # ...insert your data here...
    )
)
```

## Configuration Options

When initializing the `Autopilot` class, you can configure it using the following parameters:

1. **client (`AsyncOpenAI`)**: The OpenAI client instance. It should be an instance of `AsyncOpenAI`. If not provided, it defaults to `None`.

2. **process_fn (Callable)**: The processing function that defines how each item in the data list is processed. It should be an asynchronous function that accepts parameters `worker_id`, `client`, `data_id`, and `messages`, and returns a coroutine with a string response. If not provided, it defaults to `None`.

3. **concurrency (`int`)**: Determines the number of concurrent workers that process the data. The default value is 5.

4. **tmp_dir (`str`)**: The directory path for storing temporary files used in checkpointing. Defaults to `"tmp"`.

5. **tmp_file_prefix (`str`)**: The prefix for naming temporary files. Defaults to `"data"`.

6. **verbose (`bool`)**: A boolean flag to enable verbose logging. Useful for debugging. Defaults to `False`.

These parameters allow you to customize the behavior of the Autopilot framework according to your specific requirements.

## Example

In our example, we demonstrate how to use the Autopilot for processing requests with OpenAI's GPT-4 model. This example generates recipes for various food items. The results are outputted in a JSON format, providing an easy-to-read display of the generated recipes.

```shell
export OPENAI_API_KEY='...your api key...'
python examples/simple_process.py
```

## License

`openai-autopilot` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Acknowledgments

Thanks to ChatGPT for invaluable assistance in creating this document.
