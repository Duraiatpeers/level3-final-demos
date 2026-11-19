# Demo runbook: M3.4 and M3.5 (about 55 minutes)

Everything runs against the PX Service Assistant in `px-service-assistant/`. Commands are PowerShell. Use short folder paths.

## One-time setup (do this before the session)

1. App: `cd px-service-assistant`, `pip install -r requirements.txt`, set the four `AZURE_OPENAI_*` variables and `REQUIRE_LEARNER_MODEL=0`, then `python -m uvicorn app.main:app --port 8000`. Open `http://localhost:8000/health`, it must say `"status":"ok"`.
2. Demo packages (separate environment): `python -m venv D:\ev`, then `D:\ev\Scripts\python.exe -m pip install -r requirements-eval.txt`.
3. Promptfoo: `cd M34_Evaluation\promptfoo`, `npm.cmd install promptfoo`. Repeat in `M35_Continuous_Evaluation\promptfoo`. Needs Node.js 22.22 or newer.
4. For the judge demos, in the shell you will use set `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_CHAT_DEPLOYMENT`.
5. For M3.5, set `PX_URL=http://localhost:8000`.
6. Run the whole sequence once the day before. Real models vary, so numbers will differ from any you saw earlier.

## Sequence

Times are for you, not for the slides. Core path is the first 12 demos. Demos marked (optional) can be dropped.

| Min | Demo | Folder | Command | After slide | What to say and show |
|---|---|---|---|---|---|
| 3 | 1 Golden list in code | M34_Evaluation\programs | `python 01_golden_list.py` | 5, 6 | Four cases, one loop: dataset, run, score. Point at one FAIL and ask: bug, or just wording? |
| 4 | 2 Dataset in a file | same | `python 02_golden_from_file.py` | 6 | Same loop, 8 cases from `golden.txt`. This is how a dataset becomes versioned and reviewable. |
| 4 | 3 Repeats | same | `python 03_pass_rate_repeats.py` | 7 | Run it twice. The overall number moves. Report the average and the spread, never one run. |
| 3 | 4 Save and compare runs | same | `python 04_save_run.py`, then `python 05_compare_runs.py` | 7 | A comparison between saved runs, not between two memories. |
| 8 | 5 Promptfoo | M34_Evaluation\promptfoo | `npx.cmd promptfoo eval -c promptfooconfig.yaml --no-cache`, then `npx.cmd promptfoo view` | 11, 12 | Open the matrix in the browser: prompt versions across, tests down. Then run `promptfooconfig_judge.yaml` to show a model-graded check. |
| 7 | 6 DeepEval | M34_Evaluation\deepeval | `D:\ev\Scripts\python.exe -m pytest test_px_geval.py` | 13, 14 | It is plain pytest. Then edit the G-Eval criterion text in the file and run again. A custom metric is one sentence of criteria. |
| 2 | 7 Retrieval check | M34_Evaluation\programs | `python 06_retrieval_hit.py` | 15 | Retrieval scored apart from the answer. A MISSING line means the answer could not have been right. |
| 4 | 8 Judge, one case | same | `python 07_judge_one.py` | 8, 19 | One judge call, with tokens. Compare with the deterministic check in demo 1. |
| 5 | 9 Judge calibration | same | `python 08_collect_answers.py`, copy `..\..\extra\human_labels_sample.txt` to `human_labels.txt` (edit a few lines to match the answers you see), `python 09_judge_all.py`, `python 10_agreement.py` | 19 | Agreement number, then the two mistakes: judge too kind, judge too strict. |
| 3 | 10 Judge bias | Extra_Judge_Bias_and_Cost | `python 11_position_bias.py` | 20 | Both answers are correct. If A wins in both orders, that is position bias. |
| 3 | 11 Cost of a run | Extra_Judge_Bias_and_Cost | `python 12_cost_estimate.py` | 21 | Edit the two price lines first. One case, then three tiers. |
| 3 | 12 Fixed-threshold gate | M35_Continuous_Evaluation\programs | `python 01_gate_fixed_threshold.py`, then `echo $LASTEXITCODE` | 26 | The exit code is the gate. Pipelines read exactly this. |
| 4 | 13 Baseline and noise | same | `python 02_make_baseline.py`, `python 04_noise.py`, `python 03_gate_vs_baseline.py` | 29, 30 | The spread from 04 is why the tolerance in 03 must be at least that wide. |
| 4 | 14 What changed, then a bad candidate | same | `python 05_what_changed.py`; change `prompt_version` or the deployment; `python 05_what_changed.py` again; then `python 06_candidate_vs_baseline.py` | 31, 33 | 05 tells you which trigger fired. 06 sends the candidate through the same gate. |
| 3 | 15 The pipeline file | M35_Continuous_Evaluation | open `azure-pipelines.yml`, then Azure DevOps Repos > Branches > Branch policies > Build validation | 27 | Stages top to bottom. Pipeline alone only reports; the branch policy makes it blocking. Do not run it live. |
| 5 | 16 Online, shadow, canary | M35_Continuous_Evaluation\programs | `python 07_sample_traffic.py`, `python 08_shadow.py`, `python 09_canary.py` | 34, 36, 37 | 07: sampled reference-free checks catch a leak. 08: the user sees only v1. 09: small share, compare failure rates, keep going or roll back. |
| (opt) | Promptfoo in the pipeline | M35_Continuous_Evaluation\promptfoo | `npx.cmd promptfoo eval -c promptfooconfig_ci.yaml --no-cache -o results.junit.xml` | 27 | JUnit output is what the pipeline publishes. |

Core path total: about 55 minutes. To get to 45, drop demos 2, 4 and 7.

## If a demo misbehaves
- Real model answers vary. A FAIL on a case you expected to pass is a talking point: ask whether it is a bug, wording or drift.
- A 502 from the app means the Azure content filter refused a question. Re-run.
- `answers.txt` and `human_labels.txt` must have the same number of lines (16).
- Do not run 09_canary or 07_sample_traffic first without the app running.

## What was and was not tested
All programs ran end to end against this app in offline stub mode, and the judge programs against a stand-in model. Promptfoo, DeepEval, the Azure DevOps pipeline and the real Azure judge calls were not run here. Run the full sequence once on your machine.
