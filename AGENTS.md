# Quantum Codes Frontier agent guide

This is the only canonical agent guide for this repository. The scientific
source of truth is Git plus the current Vela repository manifest; generated
vendor-specific instruction copies are intentionally not used.

## Agent rules

Agents may:

- inspect state and exact objects with `status`, `next`, `show`, `why`, and
  `replay`
- inspect one offered Target with the write-free `vela start` briefing
- run the exact verifier named by that Target
- retain one signed, bounded Submission binding the exact packet and verifier
- propose an exact correction or supersession of one accepted Claim without
  inventing a Target, provided the Submission binds the full
  predecessor Claim ID and root

Agents may not:

- invoke repository-authority decisions or use authority credentials
- treat verifier success, Git publication, or a model answer as acceptance
- hand-edit `.vela/authority/`, `.vela/repository.json`, or retained records

## Fast commands

```bash
vela status . --json
vela next . --json
vela start <target> --frontier . --json
vela submit --frontier . --claim "<bounded result>" \
  --type computational --replayability exact \
  --artifact <path>:<kind> --caveat "<scope limit>" \
  --packet-root <packet_sha256> --profile-root <profile_sha256> \
  --verifier-capsule-root <capsule_sha256> \
  --result-contract-root <contract_sha256> \
  --as agent:<name> --json
vela submit --frontier . --claim "<bounded replacement>" \
  --type computational --replayability exact \
  --artifact <path>:<kind> --caveat "<scope limit>" \
  --supersedes <full-vcl-id> --target-root <full-sha256-root> \
  --as agent:<name> --json
vela verification import . <verification.json> --as verifier:<name> --json
vela show . <object_id> --json
vela why . <claim_id> --json
vela replay . --json
```

No current Target Index is configured. If `vela next` returns no offers,
do not invent one for already-complete evidence. Inspect existing records and
use the exact correction or supersession path only when retained evidence
actually changes one accepted Claim.
