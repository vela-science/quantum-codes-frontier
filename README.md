# Quantum codes: stabilizer `[[n,k,d]]` certificates

This current Vela repository records stabilizer-code Claims and retained
evidence. `.vela/origin.json` binds the compacted predecessor,
`.vela/repository.json` indexes current objects, `.vela/authority/` holds
repository authority, and `records/` contains content-addressed scientific
records. Git publishes bytes; it does not grant scientific authority.

The current epoch has no configured Target Index, so `vela next` returns no
offers rather than silently reviving a retired queue:

```bash
vela status . --json
vela next . --json
vela replay . --json
```

The predecessor remains available at `pre-compaction/14219ad10db5`. The
retained witness was already complete, so registering its result did not need a
retroactive Target or Attempt. Vela's exact supersession path bound the prior
open-question Claim by full ID and root. Two scoped Verification Records passed,
and a separate authorized human Decision accepted the bounded replacement
Claim. Verification did not cause acceptance.

The retained quantum witness has a source-visible alternate-algorithm
reconstruction relative to the historical capsule:

```bash
python3 scripts/verify_quantum_certificate.py \
  artifacts/quantum-10-1-4.witness.json
python3 -m unittest discover -s tests -p 'test_quantum_certificate.py' -v
```

It derives the complete phase-free binary-symplectic centralizer, enumerates
all 1,536 centralizer-minus-stabilizer representatives, and computes exact
distance four. This result is bound by the non-authoritative verifier contract at
`verifiers/quantum-10-1-4-centralizer.v1.json`. It is mechanical evidence only.

Two current Verification Records retain the scoped mathematical result and the
exact contract replay. The replay used the retained implementation with network
and file writes denied and reproduced the contract's required stdout digest.
Both records disclose the same operator, machine, repository, witness, and
implementation; they provide actor separation, not external-participant
independence or an audit of verifier soundness.

Proposal `vpr_8715dbb5e2a12442` is accepted. Its Decision establishes only that
this exact retained witness defines an explicit `[[10,1,4]]` stabilizer code;
it does not establish optimality, uniqueness, novelty, classification, or
external-participant replication. Strict repository replay remains the
publication gate.
