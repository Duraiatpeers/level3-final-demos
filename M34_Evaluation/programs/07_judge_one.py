# ----------------------------------------------------------------------
# Demo 8: one LLM-as-judge call (slides 8, 19)
# ----------------------------------------------------------------------
# Sends one question, the expected fact and one answer to a judge model and prints PASS or FAIL with a reason and the tokens used.
#
# Before you run:
#   - Set in this window: AZURE_OPENAI_ENDPOINT (full https:// address), AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHAT_DEPLOYMENT, AZURE_OPENAI_API_VERSION=2025-04-01-preview.
#   - The packages come from the 'openai' library (see README step 2).
#
# Run:     py 07_judge_one.py
# Expect:  PASS or FAIL, one sentence of reason, and the token count.
# ----------------------------------------------------------------------

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview"),
)
deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

question = "What is the maximum operating pressure of the PX-100?"
expected = "10 bar"
answer = "The PX-100 can run at up to 10 bar."

prompt = (
    "You are checking an answer from a service assistant.\n"
    "Question: " + question + "\n"
    "The correct fact: " + expected + "\n"
    "Answer given: " + answer + "\n"
    "Does the answer state the correct fact? Reply with PASS or FAIL on the first line, then one short sentence of reason."
)

response = client.chat.completions.create(
    model=deployment,
    messages=[{"role": "user", "content": prompt}],
)

print(response.choices[0].message.content)
print("Tokens used:", response.usage.total_tokens)
