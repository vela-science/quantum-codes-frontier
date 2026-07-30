# Quantum codes frontier — agent charter

This is a current Vela repository. `.vela/epoch.json` binds its signed
predecessor, `.vela/repository.json` indexes current objects,
`.vela/authority/` holds repository authority, and `records/` contains
content-addressed scientific records. `vela agents sync` regenerates tool
adapters from this file.

## Agent rules

Agents may:

- inspect state and exact objects with `status`, `next`, `show`, `why`, and
  `check --strict`
- start one offered Target when a current Target Index exists
- run the exact verifier named by that Target
- register one signed, bounded Submission from the active Attempt
- propose an exact correction or supersession of one accepted Claim without
  inventing a Target or Attempt, provided the Submission binds the full
  predecessor Claim ID and root

Agents may not:

- invoke repository-authority decisions or use authority credentials
- treat verifier success, Git publication, or a model answer as acceptance
- hand-edit `.vela/authority/`, `.vela/repository.json`, or retained records

## Fast commands

```bash
vela status . --json
vela next . --json
vela start <target> --as agent:<name> --json
vela submit --frontier . --attempt <vat_id> --claim "<bounded result>" \
  --type computational --replayability exact \
  --artifact <path>:<kind> --caveat "<scope limit>" \
  --as agent:<name> --json
vela submit --frontier . --claim "<bounded replacement>" \
  --type computational --replayability exact \
  --artifact <path>:<kind> --caveat "<scope limit>" \
  --supersedes <full-vcl-id> --target-root <full-sha256-root> \
  --as agent:<name> --json
vela show . <object_id> --json
vela why . <claim_id> --json
vela check . --strict --json
```

No current Target Index is configured. If `vela next` returns no offers,
do not invent one for already-complete evidence. Inspect existing records and
use the exact correction or supersession path only when retained evidence
actually changes one accepted Claim.
