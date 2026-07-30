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

The predecessor remains available at
`pre-current-epoch/b1f5488187a7`. A new offer must be expressed in the current
Target Index format before an agent may run `start -> submit`.

The retained quantum witness has a source-visible independent reconstruction:

```bash
python3 scripts/verify_quantum_certificate.py \
  artifacts/quantum-10-1-4.witness.json
python3 -m unittest -v tests/test_quantum_certificate.py
```

It derives the complete binary-symplectic centralizer, enumerates all 1,536
non-stabilizer logical Paulis, and computes exact distance four. This result is
mechanical evidence only. It is not yet a current Vela Verification Record,
does not change Standing, and does not make repository-wide `vela reproduce .`
green. Strict repository verification remains the publication gate.
