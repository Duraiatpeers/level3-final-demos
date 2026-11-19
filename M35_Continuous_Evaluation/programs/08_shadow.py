# ----------------------------------------------------------------------
# Demo 16b: shadow deployment (slide 36)
# ----------------------------------------------------------------------
# Sends each golden question to the current and the candidate prompt version.
# Only the current answer is 'shown to the user'; the candidate answer is only compared and logged.
#
# Before you run:
#   - Set $env:PX_URL = "http://localhost:8000" in this window (and $env:PX_KEY if the app uses a key). The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#
# Run:     py 08_shadow.py
# Expect:  One line per question with the current and candidate result, and how many questions the candidate would have made worse.
# ----------------------------------------------------------------------

import os
import sys
import requests

base = os.environ.get("PX_URL", "http://localhost:8000")
url = base + "/ask"
headers = {"X-API-Key": os.environ.get("PX_KEY", "")}

current_version = "v1"
candidate_version = "v2_1"

worse = 0
total = 0

with open("golden.txt") as file:
    for line in file:
        parts = line.strip().split("|")
        results = {}
        for version in [current_version, candidate_version]:
            body = {"question": parts[0], "prompt_version": version}
            response = requests.post(url, headers=headers, json=body)
            if response.status_code == 200:
                data = response.json()
                results[version] = [parts[1] in data["answer"], data["latency_ms"]]
            else:
                results[version] = [False, 0]
        total = total + 1
        current_ok = results[current_version][0]
        candidate_ok = results[candidate_version][0]
        if current_ok and not candidate_ok:
            worse = worse + 1
        print(parts[0][:45], "| current:", current_ok, "| candidate:", candidate_ok)

print("The user only ever sees the", current_version, "answer.")
print("Questions where the candidate would have been worse:", worse, "of", total)
