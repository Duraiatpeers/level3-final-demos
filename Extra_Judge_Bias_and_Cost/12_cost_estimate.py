# ----------------------------------------------------------------------
# Demo 11: the cost of one evaluation run (slide 21)
# ----------------------------------------------------------------------
# Measures the tokens of one app call and one judge call, then estimates the cost of three evaluation tiers.
#
# Before you run:
#   - The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#   - Set in this window: AZURE_OPENAI_ENDPOINT (full https:// address), AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHAT_DEPLOYMENT, AZURE_OPENAI_API_VERSION=2025-04-01-preview.
#   - Edit PRICE_IN and PRICE_OUT near the top to your own prices per 1 million tokens.
#
# Run:     py 12_cost_estimate.py
# Expect:  The cost of one case and an estimate for each tier.
# ----------------------------------------------------------------------

import os
import requests
from openai import AzureOpenAI

# Edit these to your own deployment prices (per 1 million tokens).
PRICE_IN = 0.40    # EDIT: price per 1 million input tokens
PRICE_OUT = 1.60   # EDIT: price per 1 million output tokens

url = "http://localhost:8000/ask"
headers = {"X-API-Key": "your-key-here"}

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview"),
)
deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

question = "What is the maximum operating pressure of the PX-100?"

# 1. Measure one app call
r = requests.post(url, headers=headers, json={"question": question, "prompt_version": "v1"})
usage = r.json()["usage"]
app_in = usage["prompt_tokens"]
app_out = usage["completion_tokens"]

# 2. Measure one judge call
judge = client.chat.completions.create(
    model=deployment,
    messages=[{"role": "user", "content": "Question: " + question + "\nAnswer: " + r.json()["answer"] + "\nReply PASS or FAIL."}],
)
j_in = judge.usage.prompt_tokens
j_out = judge.usage.completion_tokens

one_case = (app_in + j_in) * PRICE_IN / 1000000 + (app_out + j_out) * PRICE_OUT / 1000000
print("Cost of one case (app + judge): $", round(one_case, 5))
print()

# 3. Three tiers from the slide
tiers = [
    ["Tier 1: every change", 20, 1, False],
    ["Tier 2: before merge", 100, 3, True],
    ["Tier 3: scheduled", 300, 5, True],
]
for name, cases, repeats, uses_judge in tiers:
    per_case = one_case if uses_judge else (app_in * PRICE_IN + app_out * PRICE_OUT) / 1000000
    print(name, "|", cases, "cases x", repeats, "repeats = $", round(cases * repeats * per_case, 3))
