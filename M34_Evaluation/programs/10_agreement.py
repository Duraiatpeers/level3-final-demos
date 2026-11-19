# ----------------------------------------------------------------------
# Demo 9c: how often the judge agrees with the human labels (slide 19)
# ----------------------------------------------------------------------
# Compares human_labels.txt with judge_labels.txt and reports agreement.
# Also shows the two kinds of mistake: judge too kind (passes what a human fails) and too strict.
#
# Before you run:
#   - Both human_labels.txt and judge_labels.txt must exist in this folder.
#
# Run:     py 10_agreement.py
# Expect:  Agreement percent and the counts of each kind of disagreement.
# ----------------------------------------------------------------------

human = {}
judge = {}

with open("human_labels.txt") as file:
    for line in file:
        parts = line.strip().split("|")
        human[parts[0]] = parts[1].upper()

with open("judge_labels.txt") as file:
    for line in file:
        parts = line.strip().split("|")
        judge[parts[0]] = parts[1].upper()

same = 0
total = 0
judge_too_kind = 0
judge_too_strict = 0

for number in human:
    if number in judge:
        total = total + 1
        if human[number] == judge[number]:
            same = same + 1
        else:
            print("Disagree on answer", number, "| human:", human[number], "| judge:", judge[number])
            if judge[number] == "PASS":
                judge_too_kind = judge_too_kind + 1
            else:
                judge_too_strict = judge_too_strict + 1

print("Agreement:", same, "of", total, "=", round(same / total * 100), "percent")
print("Judge said PASS where the human said FAIL:", judge_too_kind)
print("Judge said FAIL where the human said PASS:", judge_too_strict)
