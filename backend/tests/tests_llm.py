#!/usr/bin/env python
import os
from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv

load_dotenv()


@patch("openai.AzureOpenAI")
def test_llm_response(mock_AzureOpenAI):
    """
    Test the LLM response by mocking the AzureOpenAI client to ensure that the response
    contains the expected output without making a real API call.
    """
    # Create a fake response for the chat completions.
    fake_message = MagicMock()
    fake_message.content = "Final Answer: Paris"
    fake_choice = MagicMock()
    fake_choice.message = fake_message
    fake_response = MagicMock()
    fake_response.choices = [fake_choice]

    # Configure the mock to return our fake response.
    instance = mock_AzureOpenAI.return_value
    instance.chat.completions.create.return_value = fake_response

    from openai import AzureOpenAI  # Re-import within the test context.

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION", "2024-06-01"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        max_retries=3,
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o"),
        messages=[
            {
                "role": "system",
                "content": "Answer the query directly. Example: Input 'What is 2+2?' → Output 'Final Answer: 4'.",
            },
            {"role": "user", "content": "What is the capital of France?"},
        ],
        temperature=0.1,
        max_tokens=150,
    )

    assert "Paris" in response.choices[0].message.content


if __name__ == "__main__":
    pytest.main()
