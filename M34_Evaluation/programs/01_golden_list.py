# ----------------------------------------------------------------------
# Demo 1: a golden list in code (slides 5, 6)
# ----------------------------------------------------------------------
# Asks the app four fixed questions and checks that each answer contains the expected fact.
# This is the smallest possible evaluation: dataset, run, score.
#
# Before you run:
#   - The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#
# Run:     py 01_golden_list.py
# Expect:  PASS or FAIL per question and a total. A FAIL can be a real bug or just different wording.
# ----------------------------------------------------------------------

import requests

url = "http://localhost:8000/ask"
headers = {"X-API-Key": "your-key-here"}

golden = [
    ["What is the maximum operating pressure of the PX-100?", "10 bar"],
    ["How often does the PX-200 need preventive maintenance?", "3 months"],
    ["Lubricant replacement interval for the PX-100?", "12 months"],
    ["max flow rate px 200??", "80"],
]

passed = 0

for item in golden:
    body = {"question": item[0], "prompt_version": "v1"}
    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        print("NO ANSWER |", item[0])
    elif item[1] in response.json()["answer"]:
        print("PASS |", item[0])
        passed = passed + 1
    else:
        print("FAIL |", item[0])

print("Passed", passed, "of", len(golden))
