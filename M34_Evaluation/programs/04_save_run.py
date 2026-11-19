# ----------------------------------------------------------------------
# Demo 4a: save a run with a label (slide 7)
# ----------------------------------------------------------------------
# Runs the golden set with one prompt version and appends the result to eval_runs.txt.
# Run it once as the baseline, then edit 'label' and 'version' and run it again for a candidate.
#
# Before you run:
#   - The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#   - golden.txt in the same folder. Delete eval_runs.txt first if you want a clean start.
#
# Run:     py 04_save_run.py
# Expect:  One line: label, passed, total and percent. The result is added to eval_runs.txt.
# ----------------------------------------------------------------------

import requests

url = "http://localhost:8000/ask"
headers = {"X-API-Key": "your-key-here"}

label = "v1_baseline"   # EDIT for the second run, e.g. "v2_candidate"
version = "v1"   # EDIT for the second run, e.g. "v2" or "v2_1"
repeats = 3   # how many times each question is asked

passed = 0
total = 0

with open("golden.txt") as file:
    for line in file:
        parts = line.strip().split("|")
        for i in range(repeats):
            body = {"question": parts[0], "prompt_version": version}
            response = requests.post(url, headers=headers, json=body)
            total = total + 1
            if response.status_code == 200 and parts[1] in response.json()["answer"]:
                passed = passed + 1

rate = round(passed / total * 100)

with open("eval_runs.txt", "a") as file:
    file.write(label + "|" + str(passed) + "|" + str(total) + "|" + str(rate) + "\n")

print(label, "passed", passed, "of", total, "=", rate, "percent")
