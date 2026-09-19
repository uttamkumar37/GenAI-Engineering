from __future__ import annotations

import abc
import json
from dataclasses import dataclass

import boto3


@dataclass
class CompletionResult:
    provider: str
    text: str


class ProviderError(Exception):
    pass


class LLMProvider(abc.ABC):
    """Same interface as the Topic 01/05 provider abstraction — drop-in swap."""

    name: str

    @abc.abstractmethod
    async def complete(self, prompt: str) -> CompletionResult: ...


class BedrockProvider(LLMProvider):
    name = "bedrock"

    def __init__(self, model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0", region: str = "us-east-1") -> None:
        self._model_id = model_id
        # expects AWS credentials via standard boto3 chain (env vars / instance role / ~/.aws/credentials)
        self._client = boto3.client("bedrock-runtime", region_name=region)

    async def complete(self, prompt: str) -> CompletionResult:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        try:
            response = self._client.invoke_model(
                modelId=self._model_id,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json",
            )
        except Exception as exc:  # boto3 raises botocore.exceptions.ClientError
            raise ProviderError(f"{self.name} invoke_model failed: {exc}") from exc

        payload = json.loads(response["body"].read())
        text = "".join(block.get("text", "") for block in payload.get("content", []))
        return CompletionResult(provider=self.name, text=text)
