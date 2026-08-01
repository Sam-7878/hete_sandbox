# Comparative evaluation report

All values below are generated from the validated 810-record JSONL corpus.

## access-only

| Metric | Numerator | Denominator | Rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| BRSR | 30 | 30 | 100.00% | 88.65%–100.00% |
| CER | 0 | 90 | 0.00% | 0.00%–4.09% |
| FCR | 0 | 30 | 0.00% | 0.00%–11.35% |
| MESR | 180 | 180 | 100.00% | 97.91%–100.00% |
| OCA | 270 | 270 | 100.00% | 98.60%–100.00% |
| SIVR | 0 | 0 | N/A | N/A |

Latency (µs): n=270, min=9436, P50=10195, P95=24207, max=97958, mean=11992.12, population σ=7231.59.

## transition-only

| Metric | Numerator | Denominator | Rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| BRSR | 30 | 30 | 100.00% | 88.65%–100.00% |
| CER | 0 | 90 | 0.00% | 0.00%–4.09% |
| FCR | 15 | 30 | 50.00% | 33.15%–66.85% |
| MESR | 90 | 180 | 50.00% | 42.77%–57.23% |
| OCA | 270 | 270 | 100.00% | 98.60%–100.00% |
| SIVR | 0 | 135 | 0.00% | 0.00%–2.77% |

Latency (µs): n=270, min=9304, P50=10415, P95=15596, max=24569, mean=11068.26, population σ=2016.05.

## full-pbea

| Metric | Numerator | Denominator | Rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| BRSR | 30 | 30 | 100.00% | 88.65%–100.00% |
| CER | 90 | 90 | 100.00% | 95.91%–100.00% |
| FCR | 30 | 30 | 100.00% | 88.65%–100.00% |
| MESR | 0 | 180 | 0.00% | 0.00%–2.09% |
| OCA | 270 | 270 | 100.00% | 98.60%–100.00% |
| SIVR | 0 | 240 | 0.00% | 0.00%–1.58% |

Latency (µs): n=270, min=9536, P50=10549, P95=187731, max=402531, mean=32904.17, population σ=67488.68.
