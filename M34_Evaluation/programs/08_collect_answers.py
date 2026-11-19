# ----------------------------------------------------------------------
# Demo 9a: collect answers for judge calibration (slide 19)
# ----------------------------------------------------------------------
# Asks the golden questions and saves the answers to answers.txt (one per line, numbered).
#
# Before you run:
#   - The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#   - golden.txt in the same folder.
#
# Run:     py 08_collect_answers.py
# Expect:  answers.txt. Then create human_labels.txt with lines like 1|PASS or 2|FAIL, one per answer. Extra_Judge_Bias_and_Cost/human_labels_sample.txt is a starting point: edit it to match the answers you see.
# ----------------------------------------------------------------------

import requests

url = "http://localhost:8000/ask"
headers = {"X-API-Key": "your-key-here"}

repeats = 2

number = 0

with open("golden.txt") as file:
    lines = file.readlines()

with open("answers.txt", "w") as out:
    for line in lines:
        parts = line.strip().split("|")
        for i in range(repeats):
            body = {"question": parts[0], "prompt_version": "v1"}
            response = requests.post(url, headers=headers, json=body)
            if response.status_code == 200:
                number = number + 1
                answer = response.json()["answer"].replace("\n", " ")
                out.write(str(number) + "|" + parts[0] + "|" + parts[1] + "|" + answer + "\n")

print("Saved", number, "answers to answers.txt")
print("Now create human_labels.txt: one line per answer, like  1|PASS  or  2|FAIL")
