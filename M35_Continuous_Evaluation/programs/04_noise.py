# ----------------------------------------------------------------------
# Demo 13b: measure the noise in the pass rate (slides 29, 30)
# ----------------------------------------------------------------------
# Runs the same golden set several times on the same build and prints the highest, lowest and spread.
# The tolerance in demo 13c must be at least as wide as this spread.
#
# Before you run:
#   - Set $env:PX_URL = "http://localhost:8000" in this window (and $env:PX_KEY if the app uses a key). The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#
# Run:     py 04_noise.py
# Expect:  Highest, lowest and spread in percentage points.
# ----------------------------------------------------------------------

import os
import sys
import requests

base = os.environ.get("PX_URL", "http://localhost:8000")
url = base + "/ask"
headers = {"X-API-Key": os.environ.get("PX_KEY", "")}

runs = 5

rates = []

for run in range(runs):
    passed = 0
    total = 0
    with open("golden.txt") as file:
        for line in file:
            parts = line.strip().split("|")
            body = {"question": parts[0], "prompt_version": "v1"}
            response = requests.post(url, headers=headers, json=body)
            total = total + 1
            if response.status_code == 200 and parts[1] in response.json()["answer"]:
                passed = passed + 1
    rate = round(passed / total * 100)
    rates.append(rate)
    print("Run", run + 1, ":", rate, "percent")

print("Lowest:", min(rates))
print("Highest:", max(rates))
print("Spread:", max(rates) - min(rates), "points")
print("A tolerance smaller than the spread will fail good builds.")
