# ----------------------------------------------------------------------
# Demo 13a: record the baseline (slide 29)
# ----------------------------------------------------------------------
# Runs the golden set several times and saves the average pass rate to baseline.txt.
#
# Before you run:
#   - Set $env:PX_URL = "http://localhost:8000" in this window (and $env:PX_KEY if the app uses a key). The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#
# Run:     py 02_make_baseline.py
# Expect:  'Baseline saved: N percent'. Creates baseline.txt.
# ----------------------------------------------------------------------

import os
import sys
import requests

base = os.environ.get("PX_URL", "http://localhost:8000")
url = base + "/ask"
headers = {"X-API-Key": os.environ.get("PX_KEY", "")}

repeats = 5

passed = 0
total = 0

with open("golden.txt") as file:
    for line in file:
        parts = line.strip().split("|")
        for i in range(repeats):
            body = {"question": parts[0], "prompt_version": "v1"}
            response = requests.post(url, headers=headers, json=body)
            total = total + 1
            if response.status_code == 200 and parts[1] in response.json()["answer"]:
                passed = passed + 1

rate = round(passed / total * 100)

with open("baseline.txt", "w") as file:
    file.write(str(rate) + "\n")

print("Baseline saved:", rate, "percent from", total, "answers")
