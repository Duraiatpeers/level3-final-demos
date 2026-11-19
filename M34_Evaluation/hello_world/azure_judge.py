# ----------------------------------------------------------------------
# Helper for demo 6: makes DeepEval use your Azure deployment as the judge
# ----------------------------------------------------------------------
# Not run directly. test_px_geval.py imports it. It uses the same AZURE_OPENAI_* settings as the app.
#
# Before you run:
#   - Set in this window: AZURE_OPENAI_ENDPOINT (full https:// address), AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHAT_DEPLOYMENT, AZURE_OPENAI_API_VERSION=2025-04-01-preview.
#
# Run:     (not run directly)
# Expect:  Nothing. Do not change this file.
# ----------------------------------------------------------------------

import os
from openai import AzureOpenAI, AsyncAzureOpenAI
from deepeval.models import DeepEvalBaseLLM


class AzureJudge(DeepEvalBaseLLM):
    """The judge model for DeepEval. It uses the same AZURE_OPENAI_* settings as the app."""

    def __init__(self):
        self.deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]
        self.settings = dict(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview"),
        )
        super().__init__(self.deployment)

    def load_model(self):
        return AzureOpenAI(**self.settings)

    def _messages(self, prompt, schema):
        if schema is not None:
            prompt = prompt + "\n\nReply with JSON only, matching this schema:\n" + str(schema.model_json_schema())
        return [{"role": "user", "content": prompt}]

    def _result(self, text, schema):
        if schema is not None:
            return schema.model_validate_json(text)
        return text

    def generate(self, prompt, schema=None, **kwargs):
        extra = {"response_format": {"type": "json_object"}} if schema is not None else {}
        r = self.model.chat.completions.create(model=self.deployment, messages=self._messages(prompt, schema), **extra)
        return self._result(r.choices[0].message.content, schema)

    async def a_generate(self, prompt, schema=None, **kwargs):
        extra = {"response_format": {"type": "json_object"}} if schema is not None else {}
        client = AsyncAzureOpenAI(**self.settings)
        r = await client.chat.completions.create(model=self.deployment, messages=self._messages(prompt, schema), **extra)
        return self._result(r.choices[0].message.content, schema)

    def get_model_name(self):
        return self.deployment
