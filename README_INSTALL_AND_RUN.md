# Evaluation demo files: install and run (Windows PowerShell)

These are only the Python and test files. They test the PX Service Assistant app, so the app must already be running.
Every file starts with a comment block that says what it does, what to set before running, the command, and what to expect.

## 1. Folder layout
- `M34_Evaluation/programs`  : demos 1 to 4, 7 to 9 (python programs, `golden.txt`)
- `M34_Evaluation/hello_world`: two tiny first tests, one for Promptfoo and one for DeepEval (run these first)
- `M34_Evaluation/promptfoo` : demo 5
- `M34_Evaluation/deepeval`  : demo 6
- `Extra_Judge_Bias_and_Cost`: demos 10 and 11
- `M35_Continuous_Evaluation`: gates, baseline, shadow, canary, Azure DevOps pipeline
- `requirements-eval.txt`    : packages for DeepEval

Use a short folder path with no spaces or apostrophes.

## 2. Install (once)
Python 3.10 or newer, and Node.js 22.22 or newer (for Promptfoo only).

Programs (everything except DeepEval):
```
py -m pip install requests openai
```
DeepEval (separate environment):
```
python -m venv C:\ev
C:\ev\Scripts\python.exe -m pip install --upgrade pip
C:\ev\Scripts\python.exe -m pip install -r requirements-eval.txt
```
Promptfoo (run in each promptfoo folder you use):
```
cd M34_Evaluation\promptfoo
npm.cmd install promptfoo
npx.cmd promptfoo --version
```
Use `npm.cmd` and `npx.cmd`; plain `npm` can be blocked by PowerShell.

## 3. The app must be running
Start it from its own folder (`px-service-assistant`), then check `http://localhost:8000/health` says `"status":"ok"` and `"mode":"azure"`.
Do not set `AZURE_OPENAI_API_VERSION` to `2026-03-17`: it fails on this resource. Use `2025-04-01-preview`.

## 4. Settings per window
Variables last only for the PowerShell window where you set them. Set these in each window that needs them.

Programs that only call the app (demos 1 to 4, 7, and all of M3.5):
```
$env:PX_URL = "http://localhost:8000"
```
Programs and tests that use the judge model (demos 8, 9, 10, 11, DeepEval):
```
$env:AZURE_OPENAI_ENDPOINT = "https://<your-resource>.services.ai.azure.com/"
$env:AZURE_OPENAI_API_KEY = "<your key>"
$env:AZURE_OPENAI_API_VERSION = "2025-04-01-preview"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT = "<your chat deployment name>"
```
Use the full `https://` address. If a judge program fails, run `py M34_Evaluation\programs\00_check_judge_connection.py` and read which line says WORKS.

## 5. Run order for M3.4
First, the hello worlds (from `M34_Evaluation\hello_world`): `npx.cmd promptfoo eval -c hello_promptfoo.yaml --no-cache` needs no app and no key; `pytest .\test_hello_deepeval.py -v -s` needs only the Azure settings in section 4. If both pass, the tools are installed correctly.

From `M34_Evaluation\programs`: `01_golden_list.py`, `02_golden_from_file.py`, `03_pass_rate_repeats.py`, `04_save_run.py` (twice, editing label and version), `05_compare_runs.py`, `06_retrieval_hit.py`, `07_judge_one.py`, `08_collect_answers.py`, then make `human_labels.txt`, then `09_judge_all.py`, `10_agreement.py`.
Promptfoo: from `M34_Evaluation\promptfoo`, `npx.cmd promptfoo eval -c promptfooconfig.yaml --no-cache`, then `npx.cmd promptfoo view`.
DeepEval: from `M34_Evaluation\deepeval`, `pytest .\test_px_geval.py -v`. Do not run it with `py`; that prints nothing.
Extra: from `Extra_Judge_Bias_and_Cost`, `py 11_position_bias.py`, `py 12_cost_estimate.py`.

Run a program like this: `py 01_golden_list.py`

## 6. Steps for M3.5
All commands run from `M35_Continuous_Evaluation\programs` with `$env:PX_URL` set and the app running. Each program exits with code 0 for pass and 1 for fail; see it with `echo $LASTEXITCODE`.

1. Fixed-threshold gate: `py 01_gate_fixed_threshold.py`, then `echo $LASTEXITCODE`. Edit `threshold` to see it fail.
2. Record the baseline: `py 02_make_baseline.py` (creates `baseline.txt`).
3. Measure the noise: `py 04_noise.py`. The spread tells you how wide the tolerance must be.
4. Gate against the baseline: `py 03_gate_vs_baseline.py`. Edit `tolerance` to see the effect.
5. What changed: `py 05_what_changed.py`. Change a setting (prompt version or deployment), run it again.
6. Candidate against the baseline: `py 06_candidate_vs_baseline.py` (candidate uses top_k 1 by default). To test another model, set `$env:CANDIDATE_DEPLOYMENT`, `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` first.
7. Sampled online checks: `py 07_sample_traffic.py`.
8. Shadow: `py 08_shadow.py`.
9. Canary: `py 09_canary.py`.
10. Pipeline: do not run it locally. Open `azure-pipelines.yml`; its header lists the Azure DevOps setup. The blocking gate is the branch policy: Repos > Branches > Branch policies > Build validation.
11. Promptfoo in the pipeline format (optional): from `M35_Continuous_Evaluation\promptfoo`, install Promptfoo, set `PX_URL`, run `npx.cmd promptfoo eval -c promptfooconfig_ci.yaml --no-cache -o results.junit.xml`.

Delete `baseline.txt`, `last_run.txt` and `eval_runs.txt` to start a demo from a clean state.

## 7. Common problems
- `NO ANSWER` in a program: the app returned an error. Check the app window; a 502 with `APIConnectionError` means the endpoint in the app window lacks `https://`.
- `No module named requests`: run `py -m pip install requests openai`.
- 404 from a judge program: API version. Use `2025-04-01-preview`.
- DeepEval test prints nothing: you ran it with `py`; use `pytest`.
