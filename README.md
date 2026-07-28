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

The retained quantum witness needs a current verifier capsule before
repository-wide `vela reproduce .` can be claimed as green. Until then, strict
repository verification is the publication gate and no broader scientific
claim is implied.
