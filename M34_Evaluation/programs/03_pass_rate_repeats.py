# ----------------------------------------------------------------------
# Demo 3: one run is not a result (slide 7)
# ----------------------------------------------------------------------
# Asks every golden question several times and reports how many passes each question got, then an overall pass rate.
#
# Before you run:
#   - The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#   - golden.txt in the same folder.
#
# Run:     py 03_pass_rate_repeats.py   (run it twice and compare)
# Expect:  Lines like '2 of 3 | question' and an overall percent. The percent changes between runs: report the average and the spread.
# ----------------------------------------------------------------------

import requests

url = "http://localhost:8000/ask"
headers = {"X-API-Key": "your-key-here"}

repeats = 3

all_passed = 0
all_total = 0

with open("golden.txt") as file:
    for line in file:
        parts = line.strip().split("|")
        question = parts[0]
        expected = parts[1]
        passed = 0
        for i in range(repeats):
            body = {"question": question, "prompt_version": "v1"}
            response = requests.post(url, headers=headers, json=body)
            if response.status_code == 200 and expected in response.json()["answer"]:
                passed = passed + 1
        print(passed, "of", repeats, "|", question)
        all_passed = all_passed + passed
        all_total = all_total + repeats

print("Overall pass rate:", round(all_passed / all_total * 100), "percent")
