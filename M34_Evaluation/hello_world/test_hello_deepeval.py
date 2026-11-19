# ----------------------------------------------------------------------
# Hello World 2: the smallest DeepEval test (no PX app needed, uses your Azure judge)
# ----------------------------------------------------------------------
# Purpose: prove that DeepEval, pytest and your Azure judge all work, before you try the real PX tests.
# The "answers" are typed in below, so the PX app does not need to be running.
# One test shows a good answer scoring high. The other shows a wrong answer scoring low.
# Both tests PASS when DeepEval behaves as expected.
#
# Install (once):  see README_INSTALL_AND_RUN.md, or:  py -m pip install deepeval==4.3.* openai pytest
# Before you run:
#   - Set in this window: AZURE_OPENAI_ENDPOINT (full https:// address), AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHAT_DEPLOYMENT, AZURE_OPENAI_API_VERSION=2025-04-01-preview.
#   - azure_judge.py (a copy is already in this folder) must stay next to this file.
#
# Run:     pytest .\test_hello_deepeval.py -v -s     (DO NOT run it with 'py': that prints nothing)
# Expect:  Two lines ending in PASSED. With -s you also see the score and the judge's reason for each.
# Try this: in test_good_answer, change the actual_output to "The pump is blue." and run again. The test fails.
# ----------------------------------------------------------------------

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

from azure_judge import AzureJudge

# The metric: a judge model scores the answer from 0 to 1 using this plain-language rule.
correct_metric = GEval(
    model=AzureJudge(),
    name="Correct pressure",
    criteria="The actual output states the same maximum pressure as the expected output.",
    evaluation_steps=[   # the steps the judge follows; written here so the judge does not have to invent them
        "Find the pressure value in the expected output.",
        "Check that the actual output gives the same value.",
        "Give a low score if the value is different.",
    ],
    evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
    threshold=0.5,   # EDIT: a score at or above this counts as a pass
)

EXPECTED = "The maximum operating pressure of the PX-100 is 10 bar."


def test_good_answer():
    test_case = LLMTestCase(
        input="What is the maximum operating pressure of the PX-100?",
        actual_output="The PX-100 can operate at up to 10 bar.",   # a correct answer, worded differently
        expected_output=EXPECTED,
    )
    correct_metric.measure(test_case)
    print("score:", correct_metric.score, "| reason:", correct_metric.reason)
    assert correct_metric.score >= correct_metric.threshold    # a good answer should score high


def test_wrong_answer():
    test_case = LLMTestCase(
        input="What is the maximum operating pressure of the PX-100?",
        actual_output="The PX-100 can operate at up to 25 bar.",   # a wrong answer
        expected_output=EXPECTED,
    )
    correct_metric.measure(test_case)
    print("score:", correct_metric.score, "| reason:", correct_metric.reason)
    assert correct_metric.score < correct_metric.threshold     # a wrong answer should score low
