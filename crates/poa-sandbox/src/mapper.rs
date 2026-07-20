use std::collections::BTreeMap;
use std::path::{Component, Path};

use poa_protocol::{ProcessConstraints, UnveilPath};

use crate::EnforcementError;

pub fn pledge_string(policy: &ProcessConstraints) -> Result<String, EnforcementError> {
    let mut promises = policy.pledge_promises.clone();
    promises.sort();
    promises.dedup();
    if promises
        .iter()
        .any(|p| p.is_empty() || p.contains(char::is_whitespace))
    {
        return Err(EnforcementError::InvalidPolicy(
            "invalid pledge promise".into(),
        ));
    }
    Ok(promises.join(" "))
}

pub fn normalized_unveil(policy: &ProcessConstraints) -> Result<Vec<UnveilPath>, EnforcementError> {
    let mut paths = BTreeMap::<String, String>::new();
    for item in &policy.unveil_paths {
        let path = Path::new(&item.path);
        if !path.is_absolute()
            || path
                .components()
                .any(|c| matches!(c, Component::ParentDir | Component::Prefix(_)))
        {
            return Err(EnforcementError::InvalidPolicy(format!(
                "non-normalized unveil path: {}",
                item.path
            )));
        }
        let normalized = path.to_string_lossy().to_string();
        if let Some(existing) = paths.insert(normalized.clone(), item.permissions.clone()) {
            if existing != item.permissions {
                return Err(EnforcementError::InvalidPolicy(format!(
                    "conflicting permissions for {normalized}"
                )));
            }
        }
    }
    Ok(paths
        .into_iter()
        .map(|(path, permissions)| UnveilPath { path, permissions })
        .collect())
}
