# Quantum codes: stabilizer [[n,k,d]] certificates — agent charter

This frontier is driven by `vela` + `git`. The ordinary path is
`next -> work -> land -> sign`: agents stop after the routed landing; only a
human key or a previously human-signed Permit policy changes accepted state.
`vela agents sync` regenerates CLAUDE.md / AGENTS.md / editor adapters from
this file — edit here, never there.

## Agent rules

Agents may:

- inspect state: `vela status .`, `vela next .`, `vela check .`
- claim one target: `vela work <target> --as agent:<name> --json`
- land Receipt v1 work through that session: `vela land --work <target>
  --claim … --artifact … --caveat … --as agent:<name> --json`
- import a foreign producer's canonical Receipt v1: `vela land receipt.json
  --as agent:<name> --json`
- run `vela check . --strict`, and run `vela reproduce .` when the frontier
  contains frozen-verifier witnesses
- rebuild derived views: `vela frontier materialize .`

Agents may not:

- run `vela sign`, accept, reject, apply, or finalize a truth-bearing proposal
- sign with, read, or handle a human's key
- hand-edit accepted events or derived views such as `frontier.json` and proof
  packets

## Fast commands

```bash
vela next . --json                              # ranked offer
vela work <target> --as agent:<name> --json     # lease + briefing
vela land --work <target> --claim <claim> \
  --type computational --replayability exact \
  --artifact <path>:<kind> --caveat <limit> \
  --as agent:<name> --json                       # Receipt v1 + policy route
vela status . --json                             # accepted and pending state
vela check . --strict                            # replay and parity gate
vela frontier materialize .                      # rebuild derived views
git push                                         # publication; no authority
```
