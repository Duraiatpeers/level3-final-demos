# ----------------------------------------------------------------------
# Demo 14b: send a candidate through the same gate (slide 33)
# ----------------------------------------------------------------------
# Runs the golden set against a baseline setting and a candidate setting and fails the candidate if it is worse by more than the tolerance.
# By default the candidate uses top_k 1 (less context). To test a different model, set $env:CANDIDATE_DEPLOYMENT to its deployment name.
#
# Before you run:
#   - Set $env:PX_URL = "http://localhost:8000" in this window (and $env:PX_KEY if the app uses a key). The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#   - If you use CANDIDATE_DEPLOYMENT, also set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in this window.
#
# Run:     py 06_candidate_vs_baseline.py
# Expect:  Baseline and candidate pass rates, then GATE PASSED or GATE FAILED.
# ----------------------------------------------------------------------

import os
import sys
import requests

base = os.environ.get("PX_URL", "http://localhost:8000")
url = base + "/ask"
headers = {"X-API-Key": os.environ.get("PX_KEY", "")}

tolerance = 10   # EDIT: points below the baseline that are still allowed
repeats = 3

baseline_extra = {"prompt_version": "v1"}
candidate_extra = {"prompt_version": "v1", "top_k": 1}   # EDIT: the change you want to test (top_k 1 = less context)

candidate_headers = dict(headers)
candidate_deployment = os.environ.get("CANDIDATE_DEPLOYMENT", "")
if candidate_deployment != "":
    candidate_headers["X-Model-Endpoint"] = os.environ["AZURE_OPENAI_ENDPOINT"]
    candidate_headers["X-Model-Key"] = os.environ["AZURE_OPENAI_API_KEY"]
    candidate_headers["X-Model-Chat-Deployment"] = candidate_deployment


def run_suite(extra, request_headers):
    passed = 0
    total = 0
    with open("golden.txt") as file:
        for line in file:
            parts = line.strip().split("|")
            for i in range(repeats):
                body = {"question": parts[0]}
                body.update(extra)
                response = requests.post(url, headers=request_headers, json=body)
                total = total + 1
                if response.status_code == 200 and parts[1] in response.json()["answer"]:
                    passed = passed + 1
    return round(passed / total * 100)


baseline_rate = run_suite(baseline_extra, headers)
candidate_rate = run_suite(candidate_extra, candidate_headers)

print("Baseline:", baseline_extra, "->", baseline_rate, "percent")
print("Candidate:", candidate_extra, "->", candidate_rate, "percent")

if candidate_rate < baseline_rate - tolerance:
    print("GATE FAILED: the candidate is worse than the baseline by more than", tolerance, "points")
    sys.exit(1)

print("GATE PASSED: the candidate is acceptable")
