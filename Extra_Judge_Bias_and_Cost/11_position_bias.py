# ----------------------------------------------------------------------
# Demo 10: judge bias, position and length (slide 20)
# ----------------------------------------------------------------------
# Shows a judge two correct answers (one short, one long) in both orders, five times each.
# If A wins in both orders it prefers the first position. If the long answer wins in both orders it prefers length.
#
# Before you run:
#   - Set in this window: AZURE_OPENAI_ENDPOINT (full https:// address), AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHAT_DEPLOYMENT, AZURE_OPENAI_API_VERSION=2025-04-01-preview.
#
# Run:     py 11_position_bias.py
# Expect:  The five votes for each order and a short explanation of how to read them.
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
short_answer = "10 bar."
long_answer = "The PX-100 is a robust unit, and in normal service it is rated for a maximum operating pressure of 10 bar, which is comfortable for most installations."

# Both answers are correct. A fair judge should not care about the order.
pairs = [
    ["short first", short_answer, long_answer],
    ["long first", long_answer, short_answer],
]

for name, first, second in pairs:
    prompt = (
        "Question: " + question + "\n"
        "Answer A: " + first + "\n"
        "Answer B: " + second + "\n"
        "Which answer is better? Reply with only the letter A or B."
    )
    votes = []
    for i in range(5):
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": prompt}],
        )
        votes.append(response.choices[0].message.content.strip()[:1].upper())
    print(name, "->", votes, "| A won", votes.count("A"), "of 5")

print()
print("If A wins in both orders, the judge prefers the first position (position bias).")
print("If the long answer wins in both orders, it prefers length (verbosity bias).")
