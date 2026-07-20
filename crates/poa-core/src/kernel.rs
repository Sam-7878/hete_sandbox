use crate::{AbortReason, RejectReason, TransitionDescriptor, TransitionOutcome};

pub trait AacoHooks<A, S, C, O> {
    type Candidate;
    type State;

    fn authorize(&self, descriptor: &TransitionDescriptor<A, S, C, O>) -> Result<(), RejectReason>;
    fn validate(&self, descriptor: &TransitionDescriptor<A, S, C, O>) -> Result<(), RejectReason>;
    fn mutate_candidate(
        &mut self,
        descriptor: &TransitionDescriptor<A, S, C, O>,
    ) -> Result<Self::Candidate, AbortReason>;
    fn reconcile(&mut self, candidate: Self::Candidate) -> Result<(), AbortReason>;
    fn state(&self) -> &Self::State;
}

pub fn execute_transition<H, A, S, C, O>(
    hooks: &mut H,
    descriptor: &TransitionDescriptor<A, S, C, O>,
) -> TransitionOutcome
where
    H: AacoHooks<A, S, C, O>,
{
    if let Err(reason) = hooks.authorize(descriptor) {
        return TransitionOutcome::Reject(reason);
    }
    if let Err(reason) = hooks.validate(descriptor) {
        return TransitionOutcome::Reject(reason);
    }
    let candidate = match hooks.mutate_candidate(descriptor) {
        Ok(candidate) => candidate,
        Err(reason) => return TransitionOutcome::Abort(reason),
    };
    match hooks.reconcile(candidate) {
        Ok(()) => TransitionOutcome::Commit,
        Err(reason) => TransitionOutcome::Abort(reason),
    }
}

