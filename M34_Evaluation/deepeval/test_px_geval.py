# ----------------------------------------------------------------------
# Demo 6: DeepEval test with a custom G-Eval metric (slides 13, 14)
# ----------------------------------------------------------------------
# Two pytest tests. Each asks the app a question and scores the answer from 0 to 1 with a metric defined in plain language (criteria and steps below).
# Slide 14 hands-on: edit the criteria text or one of the evaluation_steps, then run again and watch the scores change.
#
# Before you run:
#   - The PX app must be running on http://localhost:8000 (see README_INSTALL_AND_RUN.md, step 3).
#   - Set in this window: AZURE_OPENAI_ENDPOINT (full https:// address), AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHAT_DEPLOYMENT, AZURE_OPENAI_API_VERSION=2025-04-01-preview.
#   - azure_judge.py must be in the same folder. Install: pip install -r ..\..\requirements-eval.txt
#
# Run:     pytest .\test_px_geval.py -v     (DO NOT run it with 'py test_px_geval.py': that prints nothing)
# Expect:  Two lines ending in PASSED (score at or above the threshold) or FAILED.
# ----------------------------------------------------------------------

import requests
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

from azure_judge import AzureJudge

url = "http://localhost:8000/ask"
headers = {"X-API-Key": "your-key-here"}

limit_metric = GEval(
    model=AzureJudge(),
    name="Correct operating limit",
    criteria="The answer gives the operating limit asked for, with its unit, for the right pump model.",
    evaluation_steps=[
        "Check that the answer contains the value that the expected output contains.",
        "Check that the unit is stated.",
        "Penalise an answer that gives a value for a different pump model.",
    ],
    evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
    threshold=0.5,   # a score at or above this passes
)


def ask_app(question):
    body = {"question": question, "prompt_version": "v1"}
    response = requests.post(url, headers=headers, json=body)
    return response.json()["answer"]


def test_px100_pressure():
    question = "What is the maximum operating pressure of the PX-100?"
    test_case = LLMTestCase(
        input=question,
        actual_output=ask_app(question),
        expected_output="The maximum operating pressure of the PX-100 is 10 bar.",
    )
    assert_test(test_case, [limit_metric])


def test_px200_maintenance():
    question = "How often does the PX-200 need preventive maintenance?"
    test_case = LLMTestCase(
        input=question,
        actual_output=ask_app(question),
        expected_output="The PX-200 needs preventive maintenance every 3 months.",
    )
    assert_test(test_case, [limit_metric])
