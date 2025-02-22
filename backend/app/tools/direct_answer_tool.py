import logging
import os

from crewai.tools import BaseTool
from openai import APIError, AzureOpenAI
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class DirectAnswerInput(BaseModel):
    query: str = Field(..., description="The user query to answer directly.")


class DirectAnswerTool(BaseTool):
    name: str = "direct_answer_tool"
    description: str = "Directly answer simple queries using Azure's LLM."
    args_schema: type[BaseModel] = DirectAnswerInput  # Fixed type annotation

    def _run(self, query: str) -> str:
        try:
            logger.debug("Initializing Azure OpenAI client")
            client = AzureOpenAI(
                api_key=os.getenv("AZURE_API_KEY"),
                api_version=os.getenv("AZURE_API_VERSION", "2024-06-01"),
                azure_endpoint=os.getenv("AZURE_API_BASE"),
                max_retries=3,
            )

            logger.debug(f"Sending query to Azure: {query}")
            response = client.chat.completions.create(
                model=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o"),
                messages=[
                    {
                        "role": "system",
                        "content": "Respond EXCLUSIVELY with: Final Answer: <response>",
                    },
                    {"role": "user", "content": query},
                ],
                temperature=0.1,
                max_tokens=150,
            )

            answer = response.choices[0].message.content
            logger.debug(f"Raw Azure response: {answer}")

            if not answer.startswith("Final Answer:"):
                answer = f"Final Answer: {answer.strip()}"

            logger.info(f"Processed answer: {answer}")
            return answer.strip()

        except IndexError as ie:
            logger.error(f"Azure response format error: {ie}")
            return "Final Answer: Error processing API response format"
        except APIError as ae:
            logger.error(f"Azure API error: {ae}")
            return "Final Answer: Service temporarily unavailable"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "Final Answer: Could not process your request"
