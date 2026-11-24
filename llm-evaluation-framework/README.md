# LLM Evaluation Framework

A small Python toolkit for recording human judgments of model responses and aggregating them into a reproducible quality report. Developed with AI assistance as a personal learning project. All examples are synthetic; no employer data or actual model benchmark results are included.

## Run

Python 3.9+; standard library only. From this directory:

```sh
python evaluate.py sample.json --output report.json
python -m unittest -v
```

JSON arrays or CSV files with the same fields are supported. Each row represents one reviewer assessment of one response, identified by case_id and model. Include response text, notes, and the three integer scores below.

## Rubric

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Accuracy | materially wrong or unsupported | partially correct | correct and supported |
| Reasoning | invalid or misleading | incomplete | sound and sufficient |
| Instruction following | misses key requirement | partially meets | meets requirements |

Sample cases: math-01 asks for 15 times 3 with explanation; source-01 asks for a date using only a passage that does not specify one. Synthetic A and B are fictional response labels. The assigned scores illustrate the rubric, not measured model performance.

The report includes per-model means, evaluated case IDs, equally weighted overall percentages and zero-score failures with reviewer notes. Compare only models evaluated on the same cases under the same rubric. Scores are human inputs, not automatic truth judgments. The tool does not call models, detect hallucinations automatically or measure inter-rater agreement. Future improvements could add multiple reviewers and paired comparisons.
