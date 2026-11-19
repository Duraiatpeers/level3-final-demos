# ----------------------------------------------------------------------
# Demo 13c: gate against the baseline with a tolerance (slides 29, 30)
# ----------------------------------------------------------------------
# Runs the golden set and fails if the pass rate is more than the tolerance below the baseline.
#
# Before you run:
#   - Set $env:PX_URL = "http://localhost:8000" in this window (and $env:PX_KEY if the app uses a key). The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#   - baseline.txt must exist (run 02_make_baseline.py first).
#
# Run:     py 03_gate_vs_baseline.py
# Expect:  This run, lowest allowed, then GATE PASSED or GATE FAILED.
# ----------------------------------------------------------------------

import os
import sys
import requests

base = os.environ.get("PX_URL", "http://localhost:8000")
url = base + "/ask"
headers = {"X-API-Key": os.environ.get("PX_KEY", "")}

tolerance = 10   # EDIT: points below the baseline that are still allowed (must be >= the noise)
repeats = 3

with open("baseline.txt") as file:
    baseline = int(file.read().strip())

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
lowest_allowed = baseline - tolerance

print("Baseline:", baseline, "percent")
print("This run:", rate, "percent")
print("Lowest allowed:", lowest_allowed, "percent")

if rate < lowest_allowed:
    print("GATE FAILED: quality dropped more than the tolerance")
    sys.exit(1)

print("GATE PASSED")
