use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

use crate::{UnsupportedClaimBehavior, ValidatedUir};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct VerifiedFact {
    pub fact_id: String,
    pub claim_type: String,
    pub key: String,
    pub value: String,
    pub provenance: String,
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(transparent)]
pub struct VerifiedFactSet(pub Vec<VerifiedFact>);

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GeneratedClaim {
    pub claim_type: String,
    pub key: String,
    pub value: String,
    pub provenance: Option<String>,
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GeneratedOutput {
    pub text: String,
    pub claims: Vec<GeneratedClaim>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OutputValidation {
    pub accepted: bool,
    pub generated_claim_count: usize,
    pub supported_claim_count: usize,
    pub unsupported_claim_count: usize,
    pub violations: Vec<String>,
}

pub fn validate_output(
    uir: &ValidatedUir,
    facts: &VerifiedFactSet,
    output: &GeneratedOutput,
) -> OutputValidation {
    let contract = &uir.as_uir().output_contract;
    let index: BTreeMap<_, _> = facts
        .0
        .iter()
        .map(|fact| {
            (
                (
                    fact.claim_type.as_str(),
                    fact.key.as_str(),
                    fact.value.as_str(),
                ),
                fact,
            )
        })
        .collect();
    let mut supported = 0;
    let mut violations = Vec::new();
    for claim in &output.claims {
        if !contract.allowed_claim_types.contains(&claim.claim_type) {
            violations.push(format!("claim type not allowed: {}", claim.claim_type));
            continue;
        }
        let fact = index.get(&(
            claim.claim_type.as_str(),
            claim.key.as_str(),
            claim.value.as_str(),
        ));
        match fact {
            Some(fact)
                if !contract.provenance_required
                    || claim.provenance.as_deref() == Some(fact.provenance.as_str()) =>
            {
                supported += 1
            }
            Some(_) => violations.push(format!("provenance mismatch: {}", claim.key)),
            None => violations.push(format!("unsupported claim: {}", claim.key)),
        }
    }
    let unsupported = output.claims.len().saturating_sub(supported);
    let accepted = unsupported == 0
        || !matches!(
            contract.unsupported_claim_behavior,
            UnsupportedClaimBehavior::Reject
        );
    OutputValidation {
        accepted,
        generated_claim_count: output.claims.len(),
        supported_claim_count: supported,
        unsupported_claim_count: unsupported,
        violations,
    }
}

pub trait Renderer {
    fn render(&mut self, uir: &ValidatedUir, facts: &VerifiedFactSet) -> GeneratedOutput;
    fn invocation_count(&self) -> u64;
}

#[derive(Default)]
pub struct MockRenderer {
    invocations: u64,
    pub inject_unsupported: bool,
}

impl MockRenderer {
    pub fn new(inject_unsupported: bool) -> Self {
        Self {
            invocations: 0,
            inject_unsupported,
        }
    }
}

impl Renderer for MockRenderer {
    fn render(&mut self, _: &ValidatedUir, facts: &VerifiedFactSet) -> GeneratedOutput {
        self.invocations += 1;
        let mut claims: Vec<_> = facts
            .0
            .iter()
            .map(|fact| GeneratedClaim {
                claim_type: fact.claim_type.clone(),
                key: fact.key.clone(),
                value: fact.value.clone(),
                provenance: Some(fact.provenance.clone()),
            })
            .collect();
        if self.inject_unsupported {
            claims.push(GeneratedClaim {
                claim_type: "numeric_fact".into(),
                key: "unsupported".into(),
                value: "999".into(),
                provenance: None,
            });
        }
        GeneratedOutput {
            text: "verified facts rendered".into(),
            claims,
        }
    }
    fn invocation_count(&self) -> u64 {
        self.invocations
    }
}

pub trait VerifiedExecutor {
    fn execute(&self, uir: &ValidatedUir) -> Result<VerifiedFactSet, String>;
}

pub struct FixtureExecutor;
impl VerifiedExecutor for FixtureExecutor {
    fn execute(&self, uir: &ValidatedUir) -> Result<VerifiedFactSet, String> {
        let value = uir.as_uir();
        let metric = value
            .semantics
            .parameters
            .get("metric")
            .cloned()
            .unwrap_or_else(|| "value".into());
        Ok(VerifiedFactSet(vec![VerifiedFact {
            fact_id: format!("{}-{metric}", value.semantics.target.entity_id),
            claim_type: "numeric_fact".into(),
            key: metric,
            value: "100".into(),
            provenance: "fixture:registry-v1".into(),
        }]))
    }
}
