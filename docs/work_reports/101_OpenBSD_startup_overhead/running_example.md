# Complementary Evaluation Reproduction

Evaluated source commit: `ed9b6c2be2349bf328ca3f67a16e1b5dc392fb62`.

Ubuntu 24.04 validates source and reports; OpenBSD 7.9 performs native enforcement. SSH and verifier ports are distinct: use an SSH port such as `22`; the example verifier uses TCP `7878`.

```sh
# OpenBSD native (30 runs)
SOURCE_COMMIT=ed9b6c2be2349bf328ca3f67a16e1b5dc392fb62 sh evaluation/runners/run_openbsd_complementary.sh \
  /path/to/hete_sandbox /path/to/output/openbsd-native 30

# Ubuntu report generation after copying native output
python3 evaluation/openbsd_startup_evidence.py \
  docs/work_reports/101_OpenBSD_startup_overhead/openbsd-native/startup-overhead-openbsd.jsonl \
  --markdown docs/work_reports/101_OpenBSD_startup_overhead/startup_overhead_openbsd.md \
  --latex docs/work_reports/101_OpenBSD_startup_overhead/generated/startup_overhead_openbsd.tex
```

Expected empty-unveil exit is 0 with ENOENT/ENOENT/EPERM observations. Invalid-policy and missing-resource exits are 1 with listener closed and no business-loop marker.
