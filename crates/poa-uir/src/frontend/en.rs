use regex::Regex;

use crate::{DslFrontend, Intent, Language, UirCompileError, UniversalIrDraft};

#[derive(Default)]
pub struct EnglishFrontend;

impl DslFrontend for EnglishFrontend {
    fn language(&self) -> Language {
        Language::En
    }

    fn compile(&self, input: &str) -> Result<UniversalIrDraft, UirCompileError> {
        super::reject_adversarial(input)?;
        let lower = input.to_lowercase();
        let intent = if lower.contains("compare") {
            Intent::Compare
        } else if lower.contains("cause") || lower.contains("trace") {
            Intent::CauseTrace
        } else if lower.contains("summarize") {
            Intent::Summarize
        } else if lower.contains("extract") {
            Intent::Extract
        } else if lower.contains("analyze") {
            Intent::Analyze
        } else if lower.contains("verify") || lower.contains("check") {
            Intent::Verify
        } else {
            return Err(UirCompileError::Incomplete("intent".into()));
        };
        let entity = capture(
            input,
            r"(?i)(?:entity|company|target)\s+([A-Z][A-Z0-9_-]{1,31})",
        )
        .ok_or_else(|| UirCompileError::Incomplete("target".into()))?;
        let metric = capture(input, r"(?i)(?:metric|field)\s+([a-z][a-z0-9_]{1,31})")
            .unwrap_or_else(|| "value".into())
            .to_lowercase();
        let year = capture(input, r"\b(20\d{2})\b").unwrap_or_else(|| "2025".into());
        super::ko::build(intent, entity.to_uppercase(), metric, year, input)
    }
}

fn capture(input: &str, pattern: &str) -> Option<String> {
    Regex::new(pattern)
        .ok()?
        .captures(input)?
        .get(1)
        .map(|value| value.as_str().to_owned())
}
