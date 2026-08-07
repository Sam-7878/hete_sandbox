use std::collections::BTreeMap;

use regex::Regex;

use crate::{
    Condition, DslFrontend, Enforcement, ExecutionContract, ExecutionMode, FailureBehavior, Intent,
    Language, OutputContract, OutputFormat, PolicyConstraint, PolicyLevel, ScalarValue, Semantics,
    Target, UirCompileError, UniversalIrDraft, UnsupportedClaimBehavior,
};

#[derive(Default)]
pub struct KoreanFrontend;

impl DslFrontend for KoreanFrontend {
    fn language(&self) -> Language {
        Language::Ko
    }

    fn compile(&self, input: &str) -> Result<UniversalIrDraft, UirCompileError> {
        super::reject_adversarial(input)?;
        let intent = if input.contains("비교") {
            Intent::Compare
        } else if input.contains("원인") || input.contains("추적") {
            Intent::CauseTrace
        } else if input.contains("요약") {
            Intent::Summarize
        } else if input.contains("추출") {
            Intent::Extract
        } else if input.contains("분석") {
            Intent::Analyze
        } else if input.contains("검증") || input.contains("확인") {
            Intent::Verify
        } else {
            return Err(UirCompileError::Incomplete("intent".into()));
        };
        let entity = capture(input, r"(?:기업|대상|엔터티)\s+([A-Z][A-Z0-9_-]{1,31})")
            .ok_or_else(|| UirCompileError::Incomplete("target".into()))?;
        let metric = capture(input, r"(?:지표|항목)\s+([a-z][a-z0-9_]{1,31})")
            .unwrap_or_else(|| "value".into());
        let year = capture(input, r"(20\d{2})년?").unwrap_or_else(|| "2025".into());
        build(intent, entity, metric, year, input)
    }
}

fn capture(input: &str, pattern: &str) -> Option<String> {
    Regex::new(pattern)
        .ok()?
        .captures(input)?
        .get(1)
        .map(|value| value.as_str().to_owned())
}

pub(crate) fn build(
    intent: Intent,
    entity: String,
    metric: String,
    year: String,
    input: &str,
) -> Result<UniversalIrDraft, UirCompileError> {
    if intent == Intent::Compare
        && !(input.contains("대비")
            || input.contains("비교")
            || input.to_ascii_lowercase().contains("compare"))
    {
        return Err(UirCompileError::Incomplete("comparison operand".into()));
    }
    let mut parameters = BTreeMap::new();
    parameters.insert("metric".into(), metric.clone());
    parameters.insert("period".into(), year.clone());
    parameters.insert("actor".into(), "research-agent".into());
    let condition = condition_from_input(input);
    let lowered = input.to_lowercase();
    let enforcement = if input.contains("차단") || lowered.contains("block") {
        Enforcement::BlockExecution
    } else if input.contains("격리") || lowered.contains("quarantine") {
        Enforcement::Quarantine
    } else if input.contains("감축") || lowered.contains("degrade") {
        Enforcement::GracefulDegradation
    } else if input.contains("허용") || lowered.contains("allow") {
        Enforcement::Bypass
    } else {
        Enforcement::Reject
    };
    Ok(UniversalIrDraft {
        semantics: Semantics {
            intent,
            target: Target {
                entity_type: "organization".into(),
                entity_id: entity,
            },
            action: "verify_fact".into(),
            parameters,
            conditions: vec![condition.clone()],
            temporal_scope: Some(year),
        },
        policy_constraints: vec![PolicyConstraint {
            id: "entity-must-exist".into(),
            level: PolicyLevel::L1Domain,
            condition,
            enforcement,
            source: "registry-policy".into(),
        }],
        execution_contract: ExecutionContract {
            required_capabilities: vec!["entity_registry".into(), "verified_fact_lookup".into()],
            required_resources: vec![metric],
            allowed_operations: vec!["verify_fact".into()],
            provenance_requirements: vec!["source_id".into()],
            failure_behavior: FailureBehavior::Reject,
            execution_mode: ExecutionMode::VerifiedOnly,
        },
        output_contract: OutputContract {
            format: OutputFormat::GroundedNaturalLanguage,
            allowed_claim_types: vec!["numeric_fact".into(), "entity_fact".into()],
            provenance_required: true,
            numeric_exactness: true,
            allow_external_inference: false,
            unsupported_claim_behavior: UnsupportedClaimBehavior::Reject,
        },
        domain: "research_finance".into(),
    })
}

fn condition_from_input(input: &str) -> Condition {
    let lowered = input.to_lowercase();
    let verified = || Condition::Eq {
        lhs: "entity_verified".into(),
        rhs: ScalarValue::Boolean(true),
    };
    let policy_verified = || Condition::Eq {
        lhs: "policy_verified".into(),
        rhs: ScalarValue::Boolean(true),
    };
    if input.contains("예외") || lowered.contains("unless") || lowered.contains("except") {
        Condition::Except {
            rule: Box::new(verified()),
            exception: Box::new(Condition::Eq {
                lhs: "exception_authorized".into(),
                rhs: ScalarValue::Boolean(true),
            }),
        }
    } else if input.contains("그리고") || lowered.contains(" and ") {
        Condition::And {
            exprs: vec![verified(), policy_verified()],
        }
    } else if input.contains("또는") || lowered.contains(" or ") {
        Condition::Or {
            exprs: vec![verified(), policy_verified()],
        }
    } else if input.contains("아님") || lowered.contains(" not ") {
        Condition::Not {
            expr: Box::new(verified()),
        }
    } else if input.contains("초과") || lowered.contains("greater than") {
        Condition::Gt {
            lhs: "threshold".into(),
            rhs: ScalarValue::Integer(0),
        }
    } else if input.contains("미만") || lowered.contains("less than") {
        Condition::Lt {
            lhs: "threshold".into(),
            rhs: ScalarValue::Integer(0),
        }
    } else {
        verified()
    }
}
