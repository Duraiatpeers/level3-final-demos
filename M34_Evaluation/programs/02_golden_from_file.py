# ----------------------------------------------------------------------
# Demo 2: the golden dataset in a file (slide 6)
# ----------------------------------------------------------------------
# Same loop as demo 1, but the cases are read from golden.txt (question|expected fact, one per line).
# Moving cases out of code is how a dataset becomes reviewable and versioned.
#
# Before you run:
#   - The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#   - golden.txt must be in the same folder.
#
# Run:     py 02_golden_from_file.py
# Expect:  PASS or FAIL for each case in golden.txt and a total.
# ----------------------------------------------------------------------

import requests

url = "http://localhost:8000/ask"
headers = {"X-API-Key": "your-key-here"}

passed = 0
total = 0

with open("golden.txt") as file:
    for line in file:
        parts = line.strip().split("|")
        question = parts[0]
        expected = parts[1]
        body = {"question": question, "prompt_version": "v1"}
        response = requests.post(url, headers=headers, json=body)
        total = total + 1
        if response.status_code == 200 and expected in response.json()["answer"]:
            print("PASS |", question)
            passed = passed + 1
        else:
            print("FAIL |", question)

print("Passed", passed, "of", total)
