# ----------------------------------------------------------------------
# Demo 14a: detect what changed since the last run (slide 31)
# ----------------------------------------------------------------------
# Reads the app's settings (/health and a test answer), compares them with last_run.txt and reports which trigger changed: model, prompt, index or settings.
# The first run only saves the settings.
#
# Before you run:
#   - Set $env:PX_URL = "http://localhost:8000" in this window (and $env:PX_KEY if the app uses a key). The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#
# Run:     py 05_what_changed.py   (run it, change a prompt version or deployment, run it again)
# Expect:  First run: 'Saved the current settings'. Later runs: the list of changes, and exit code 1 if something changed.
# ----------------------------------------------------------------------

import os
import sys
import requests

base = os.environ.get("PX_URL", "http://localhost:8000")
url = base + "/ask"
headers = {"X-API-Key": os.environ.get("PX_KEY", "")}

health = requests.get(base + "/health").json()

body = {"question": "What is the maximum operating pressure of the PX-100?", "prompt_version": "v1"}
response = requests.post(url, headers=headers, json=body)
settings = response.json()["settings"]

current = {
    "model": str(settings["model"]),
    "mode": str(health["mode"]),
    "prompt_versions": ",".join(health["prompt_versions"]),
    "indexes": ",".join(health["indexes"]),
    "chunks_in_index": str(health["chunks"]),
    "redact_personal_data": str(health["redact_personal_data"]),
}

previous = {}

if os.path.exists("last_run.txt"):
    with open("last_run.txt") as file:
        for line in file:
            parts = line.strip().split("=")
            previous[parts[0]] = parts[1]

changed = 0

for key in current:
    if key in previous and previous[key] != current[key]:
        print("CHANGED:", key, "|", previous[key], "->", current[key])
        changed = changed + 1

with open("last_run.txt", "w") as file:
    for key in current:
        file.write(key + "=" + current[key] + "\n")

if len(previous) == 0:
    print("First run. Saved the current settings.")
elif changed == 0:
    print("Nothing changed. No re-evaluation needed for these settings.")
else:
    print("Re-evaluation needed:", changed, "setting(s) changed")
    sys.exit(1)
