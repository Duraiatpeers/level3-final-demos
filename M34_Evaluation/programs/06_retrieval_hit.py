# ----------------------------------------------------------------------
# Demo 7: check retrieval apart from the answer (slide 15)
# ----------------------------------------------------------------------
# For each golden question, checks whether the text the app retrieved contains the expected fact.
# If the fact was not retrieved, the answer could not have been right, whatever the model says.
#
# Before you run:
#   - The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#
# Run:     py 06_retrieval_hit.py
# Expect:  FOUND or MISSING per question and a count. MISSING points at retrieval, not at the model.
# ----------------------------------------------------------------------

import requests

url = "http://localhost:8000/ask"
headers = {"X-API-Key": "your-key-here"}

hits = 0
total = 0

with open("golden.txt") as file:
    for line in file:
        parts = line.strip().split("|")
        body = {"question": parts[0], "prompt_version": "v1"}
        response = requests.post(url, headers=headers, json=body)
        if response.status_code != 200:
            continue
        total = total + 1
        found = False
        for chunk in response.json()["chunks"]:
            if parts[1] in chunk["text"]:
                found = True
        if found:
            hits = hits + 1
            print("FOUND   |", parts[0])
        else:
            print("MISSING |", parts[0])

print("Retrieved text contained the expected fact for", hits, "of", total)
