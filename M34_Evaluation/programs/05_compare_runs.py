# ----------------------------------------------------------------------
# Demo 4b: compare saved runs (slide 7)
# ----------------------------------------------------------------------
# Reads eval_runs.txt and compares the latest run with the first one (the baseline).
#
# Before you run:
#   - Run 04_save_run.py at least twice first, with different labels. With only one saved run it compares the baseline with itself.
#
# Run:     py 05_compare_runs.py
# Expect:  All saved runs, then REGRESSION (latest is lower) or OK (not lower).
# ----------------------------------------------------------------------

rates = []
labels = []

with open("eval_runs.txt") as file:
    for line in file:
        parts = line.strip().split("|")
        labels.append(parts[0])
        rates.append(int(parts[3]))
        print(parts[0], "->", parts[3], "percent")

baseline = rates[0]
latest = rates[-1]

if latest < baseline:
    print("REGRESSION:", labels[-1], "is", baseline - latest, "points below", labels[0])
else:
    print("OK:", labels[-1], "is not below", labels[0])
