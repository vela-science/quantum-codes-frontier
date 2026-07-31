# Quantum codes: stabilizer `[[n,k,d]]` certificates

This current Vela repository records stabilizer-code Claims and retained
evidence. `.vela/epoch.json` binds the signed predecessor,
`.vela/repository.json` indexes current objects, `.vela/authority/` holds
repository authority, and `records/` contains content-addressed scientific
records. Git publishes bytes; it does not grant scientific authority.

The current epoch has no configured Target Index, so `vela next` returns no
offers rather than silently reviving a retired queue:

```bash
vela status . --json
vela next . --json
vela check . --strict --json
```

The predecessor remains available at `pre-current-epoch/b1f5488187a7`. The
retained witness is already complete, so registering its result does not need a
retroactive Target or Attempt. Vela's exact supersession path can propose a
replacement for the accepted open-question Claim by binding its full Claim ID
and root. That Submission remains `pending_review` until a separate scoped
Verification and authorized human Decision.

The retained quantum witness has a source-visible independent reconstruction:

```bash
python3 scripts/verify_quantum_certificate.py \
  artifacts/quantum-10-1-4.witness.json
python3 -m unittest discover -s tests -p 'test_quantum_certificate.py' -v
```

It derives the complete binary-symplectic centralizer, enumerates all 1,536
non-stabilizer logical Paulis, and computes exact distance four. This result is
bound by the non-authoritative verifier contract at
`verifiers/quantum-10-1-4-centralizer.v1.json`. It is mechanical evidence only.

Two current Verification Records retain the scoped mathematical result and the
exact contract replay. The replay used the retained implementation with network
and file writes denied and reproduced the contract's required stdout digest.
Both records disclose the same operator, machine, repository, witness, and
implementation; they provide actor separation, not external-participant
independence or an audit of verifier soundness.

The Proposal remains pending an authorized human Decision. Neither Verification
changed accepted Standing. Strict repository verification remains the
publication gate.
