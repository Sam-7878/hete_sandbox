# Phase-2 Frozen-v1 Semantic Failure Diagnostic

Frozen-v1 is a retrospective diagnostic benchmark after Phase-2 and must not be described as the Phase-3 unseen holdout.

## Taxonomy

| Error type | Failures |
|---|---:|
| ACTION_SYNONYM_UNSEEN | 320 |
| COORDINATION_FAILURE | 113 |
| MORPHOLOGY_FAILURE_KO | 77 |
| SECURITY_REJECT_EXPECTED | 60 |
| INTENT_UNSEEN | 0 |
| TARGET_EXTRACTION_FAILURE | 0 |
| ENTITY_ALIAS_FAILURE | 0 |
| ATTRIBUTE_SYNONYM_FAILURE | 0 |
| TEMPORAL_SCOPE_FAILURE | 0 |
| CONDITION_ORDER_FAILURE | 0 |
| NEGATION_FAILURE | 0 |
| EXCEPTION_SCOPE_FAILURE | 0 |
| CODE_SWITCH_FAILURE | 0 |
| PREPOSITION_FAILURE_EN | 0 |
| UNSUPPORTED_SURFACE_FORM | 0 |
| AMBIGUOUS_INPUT | 0 |

## G2–G4 failure counts

| Split | Language | Failures |
|---|---|---:|
| G2_TEMPLATE_UNSEEN_ENTITY_SEEN | en | 95 |
| G2_TEMPLATE_UNSEEN_ENTITY_SEEN | ko | 95 |
| G3_TEMPLATE_UNSEEN_ENTITY_UNSEEN | en | 95 |
| G3_TEMPLATE_UNSEEN_ENTITY_UNSEEN | ko | 95 |
| G4_LEXICAL_UNSEEN | en | 95 |
| G4_LEXICAL_UNSEEN | ko | 95 |

## Interpretation

The taxonomy is diagnostic, rule-based, and auditable. It is used to improve semantic categories rather than to add case IDs or entity instances to the parser.
