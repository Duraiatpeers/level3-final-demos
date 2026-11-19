# ----------------------------------------------------------------------
# Demo 12: quality gate with a fixed threshold (slide 26)
# ----------------------------------------------------------------------
# Runs the golden set, computes the pass rate and fails the build (exit code 1) if it is below the threshold.
# The exit code is what a pipeline reads.
#
# Before you run:
#   - Set $env:PX_URL = "http://localhost:8000" in this window (and $env:PX_KEY if the app uses a key). The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#
# Run:     py 01_gate_fixed_threshold.py ; echo $LASTEXITCODE
# Expect:  Pass rate, then GATE PASSED or GATE FAILED. $LASTEXITCODE is 0 for pass and 1 for fail.
# ----------------------------------------------------------------------

import os
import sys
import requests

base = os.environ.get("PX_URL", "http://localhost:8000")
url = base + "/ask"
headers = {"X-API-Key": os.environ.get("PX_KEY", "")}

threshold = 60   # EDIT: minimum pass rate (percent) to pass the gate
repeats = 2   # how many times each question is asked

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
print("Pass rate:", rate, "percent | required:", threshold, "percent")

if rate < threshold:
    print("GATE FAILED")
    sys.exit(1)

print("GATE PASSED")
