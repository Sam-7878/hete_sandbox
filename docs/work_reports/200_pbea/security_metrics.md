# Security metrics

This file summarizes `generated/metrics.json`; that JSON is computed only after the 810-record validator succeeds.

- MESR: successful malicious effects / attempted malicious effects (lower is better).
- BRSR: successful benign S0 runs / benign S0 runs (higher is better).
- SIVR: state changes among non-commit outcomes / non-commit outcomes (lower is better).
- CER: contained S2–S4 capability attempts / S2–S4 attempts (higher is better).
- FCR: fail-closed S5 startups / S5 startups (higher is better).
- OCA: records whose observed outcome equals the independently specified outcome / all records (higher is better).

| Mode | MESR | BRSR | SIVR | CER | FCR | OCA |
|---|---:|---:|---:|---:|---:|---:|
| B0 | 180/180 (100%) | 30/30 (100%) | N/A (0 non-commit records) | 0/90 (0%) | 0/30 (0%) | 270/270 (100%) |
| B1 | 90/180 (50%) | 30/30 (100%) | 0/135 (0%) | 0/90 (0%) | 15/30 (50%) | 270/270 (100%) |
| P | 0/180 (0%) | 30/30 (100%) | 0/240 (0%) | 90/90 (100%) | 30/30 (100%) | 270/270 (100%) |

Selected Wilson 95% intervals are: P MESR 0.00%–2.09%, P CER 95.91%–100.00%, P SIVR 0.00%–1.58%, and all-mode OCA 98.60%–100.00%. Exact numerator, denominator, rate, and interval for every cell are in `generated/metrics.json` and `generated/security_metrics.tex`.
