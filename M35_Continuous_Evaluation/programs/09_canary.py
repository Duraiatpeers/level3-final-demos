# ----------------------------------------------------------------------
# Demo 16c: canary release (slide 37)
# ----------------------------------------------------------------------
# Sends a small share of requests to the candidate version and the rest to the current one, then compares failure rates and decides to roll back or keep going.
#
# Before you run:
#   - Set $env:PX_URL = "http://localhost:8000" in this window (and $env:PX_KEY if the app uses a key). The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#
# Run:     py 09_canary.py
# Expect:  Requests and failure rate for current and canary, then ROLLBACK (exit code 1) or KEEP GOING.
# ----------------------------------------------------------------------

import os
import sys
import requests

base = os.environ.get("PX_URL", "http://localhost:8000")
url = base + "/ask"
headers = {"X-API-Key": os.environ.get("PX_KEY", "")}

import random

requests_count = 30
canary_share = 0.3   # EDIT: share of requests sent to the canary
allowed_extra_failures = 20

with open("golden.txt") as file:
    golden = [line.strip().split("|") for line in file]

counts = {"current": 0, "canary": 0}
failures = {"current": 0, "canary": 0}

for number in range(requests_count):
    item = golden[number % len(golden)]
    if random.random() < canary_share:
        arm = "canary"
        version = "v2_1"
    else:
        arm = "current"
        version = "v1"
    body = {"question": item[0], "prompt_version": version}
    response = requests.post(url, headers=headers, json=body)
    counts[arm] = counts[arm] + 1
    if response.status_code != 200 or item[1] not in response.json()["answer"]:
        failures[arm] = failures[arm] + 1

for arm in ["current", "canary"]:
    if counts[arm] > 0:
        rate = round(failures[arm] / counts[arm] * 100)
    else:
        rate = 0
    print(arm, "| requests:", counts[arm], "| failures:", failures[arm], "| failure rate:", rate, "percent")

if counts["canary"] > 0 and counts["current"] > 0:
    canary_rate = failures["canary"] / counts["canary"] * 100
    current_rate = failures["current"] / counts["current"] * 100
    if canary_rate > current_rate + allowed_extra_failures:
        print("ROLLBACK: the canary fails clearly more than the current version")
        sys.exit(1)

print("KEEP GOING: no clear problem with the canary yet")
