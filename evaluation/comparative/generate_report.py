#!/usr/bin/env python3
import argparse, json, pathlib

def main():
    p=argparse.ArgumentParser(); p.add_argument("metrics",type=pathlib.Path); p.add_argument("output",type=pathlib.Path); a=p.parse_args()
    d=json.loads(a.metrics.read_text()); lines=["# Comparative evaluation report","","All values below are generated from the validated 810-record JSONL corpus.",""]
    for mode,row in d.items():
        lines += [f"## {mode}","", "| Metric | Numerator | Denominator | Rate | Wilson 95% CI |","|---|---:|---:|---:|---:|"]
        for name,m in row["metrics"].items(): lines.append(f"| {name} | {m['numerator']} | {m['denominator']} | {100*m['rate']:.2f}% | {100*m['wilson_95_low']:.2f}%–{100*m['wilson_95_high']:.2f}% |")
        x=row["latency_us"]; lines += ["",f"Latency (µs): n={x['count']}, min={x['min']}, P50={x['p50']}, P95={x['p95']}, max={x['max']}, mean={x['mean']:.2f}, population σ={x['population_stddev']:.2f}.",""]
    a.output.write_text("\n".join(lines)+"\n")
if __name__=="__main__": main()
