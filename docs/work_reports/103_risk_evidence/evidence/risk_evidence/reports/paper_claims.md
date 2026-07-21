# Evidence-bounded Paper Claims

The following wording is supported by the supplied artifacts:

1. HETE Sandbox implements RiskEvidence as an optional, domain-independent POA policy extension.
2. Risk-classified failures are deterministically routed to Reject or Quarantine according to an explicit threshold policy.
3. Quarantined pre-commit transitions do not propagate candidate state into committed state in the tested risk-aware executor.
4. RiskEvidence audit records retain typed provenance, evaluator rationale, correlation, and effective policy identity without adding domain payload or candidate state.
5. Threshold sensitivity is quantitatively reproducible on the supplied fixed synthetic corpus.
6. The extension preserves existing non-risk AACO behavior, direct Quarantine behavior, and the absent-extension golden digest in the tested configurations.
7. The evaluator performs a fixed number of scalar threshold comparisons for a single RiskEvidence record.

Each statement is limited to source commit `c2128a9603d2a14d4927bfe72e5e1caf1306c829`, the documented tests, and the recorded environments.
