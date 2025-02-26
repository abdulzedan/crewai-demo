import os

os.environ.setdefault("AZURE_API_KEY", "dummy")
os.environ.setdefault("AZURE_API_BASE", "http://dummy")


import pytest
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings


def dummy_embed_query(self, text: str):
    # Return a dummy embedding (a list of floats)
    return [0.0, 0.1, 0.2]


@pytest.fixture(autouse=True)
def patch_azure_openai_embeddings():
    # This fixture runs before any tests and patches embed_query
    AzureOpenAIEmbeddings.embed_query = dummy_embed_query
