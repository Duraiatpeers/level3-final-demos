# ----------------------------------------------------------------------
# Demo 9b: judge every collected answer (slide 19)
# ----------------------------------------------------------------------
# Reads answers.txt, asks the judge model for PASS or FAIL on each, and saves judge_labels.txt.
#
# Before you run:
#   - Set in this window: AZURE_OPENAI_ENDPOINT (full https:// address), AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHAT_DEPLOYMENT, AZURE_OPENAI_API_VERSION=2025-04-01-preview.
#   - answers.txt must exist (run 08_collect_answers.py first).
#
# Run:     py 09_judge_all.py
# Expect:  Judge calls made, tokens in and out, and judge_labels.txt.
# ----------------------------------------------------------------------

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview"),
)
deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

calls = 0
tokens_in = 0
tokens_out = 0

with open("answers.txt") as file:
    lines = file.readlines()

with open("judge_labels.txt", "w") as out:
    for line in lines:
        parts = line.strip().split("|")
        prompt = (
            "You are checking an answer from a service assistant.\n"
            "Question: " + parts[1] + "\n"
            "The correct fact: " + parts[2] + "\n"
            "Answer given: " + parts[3] + "\n"
            "Does the answer state the correct fact? Reply with PASS or FAIL on the first line, then one short sentence of reason."
        )
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.choices[0].message.content.strip()
        label = "PASS"
        if text.upper().startswith("FAIL"):
            label = "FAIL"
        out.write(parts[0] + "|" + label + "\n")
        calls = calls + 1
        tokens_in = tokens_in + response.usage.prompt_tokens
        tokens_out = tokens_out + response.usage.completion_tokens

print("Judge calls:", calls)
print("Tokens in:", tokens_in)
print("Tokens out:", tokens_out)
