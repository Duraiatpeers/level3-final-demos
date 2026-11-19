# PX Eval Demo project

- `px-service-assistant/`: the PX Service Assistant app (FastAPI RAG on Azure OpenAI). No seeded defects. `LLM_MODE=stub` runs it offline for a dry run.
- `M34_Evaluation/`: M3.4 programs, Promptfoo and DeepEval tests. Start with `hello_world/` (one tiny Promptfoo test and one tiny DeepEval test), then the numbered programs.
- `M35_Continuous_Evaluation/`: M3.5 gate, baseline, shadow and canary programs, Azure DevOps pipeline, Promptfoo CI config.
- `Extra_Judge_Bias_and_Cost/`: judge bias and cost demos, and a sample human-label file.
- `docs/Lab_Guide_M3_4_M3_5.docx`: the detailed lab guide for M3.4 and M3.5, with explanations.
- `README_INSTALL_AND_RUN.md`: install and run steps for the evaluation files only.
- `RUNBOOK.md`: setup and the demo sequence.
