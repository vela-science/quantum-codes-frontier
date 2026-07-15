# Quantum codes: stabilizer [[n,k,d]] certificates

This standalone Vela frontier owns its accepted scientific state in
`.vela/events/`. `frontier.json`, `vela.lock`, and `proof/` are deterministic
views rebuilt from that log. Git publishes the exact bytes; it does not grant
scientific authority.

The ordinary producer loop is task-first:

```bash
vela status . --json
vela next . --json
vela work <target> --as agent:<name> --json
vela land --work <target> --claim <claim> \
  --type computational --replayability exact \
  --artifact <path>:<kind> --caveat <scope-limit> \
  --as agent:<name> --json
```

Verification and deterministic regeneration:

```bash
vela check . --strict
vela frontier materialize .
```

This frontier currently has no frozen-verifier witness files. If witnesses are
added later, re-run them from scratch with `vela reproduce .`.

Agents stop after `land`. Only a key-holding human runs `vela sign` for work
that a previously signed policy did not already permit.
