# ----------------------------------------------------------------------
# Check the judge connection (run this first if a judge program fails)
# ----------------------------------------------------------------------
# Sends one tiny request to your Azure deployment using several API versions and prints which ones work.
#
# Before you run:
#   - Set in this window: AZURE_OPENAI_ENDPOINT (full https:// address), AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHAT_DEPLOYMENT, AZURE_OPENAI_API_VERSION (optional here).
#
# Run:     py 00_check_judge_connection.py
# Expect:  Lines starting WORKS show a version you can use. If all fail, the endpoint, key or deployment name is wrong.
# ----------------------------------------------------------------------

import os
from openai import AzureOpenAI, OpenAI

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
key = os.environ["AZURE_OPENAI_API_KEY"]
deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]
messages = [{"role": "user", "content": "Reply with the word OK."}]

print("Endpoint  :", endpoint)
print("Deployment:", deployment)
print("API version in this window:", os.environ.get("AZURE_OPENAI_API_VERSION", "(not set)"))
print()

for version in ["2025-04-01-preview", "2025-01-01-preview", "2024-10-21", "2026-03-17"]:
    try:
        client = AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version=version, max_retries=0)
        r = client.chat.completions.create(model=deployment, messages=messages)
        print("WORKS   | AzureOpenAI, api_version", version, "->", r.choices[0].message.content)
    except Exception as e:
        print("FAILS   | AzureOpenAI, api_version", version, "->", type(e).__name__, str(e)[:90])

try:
    base = endpoint.rstrip("/") + "/openai/v1/"
    client = OpenAI(base_url=base, api_key=key, max_retries=0)
    r = client.chat.completions.create(model=deployment, messages=messages)
    print("WORKS   | OpenAI client, base_url", base, "->", r.choices[0].message.content)
except Exception as e:
    print("FAILS   | OpenAI client, base_url /openai/v1/ ->", type(e).__name__, str(e)[:90])
