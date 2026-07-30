#!/usr/bin/env python3
"""Build the domain-owned quantum-code Target Index candidate.

Vela owns the closed v4 seal. This generator owns only the one bounded target
and validates every worktree object that determines its semantics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANDIDATE_PATH = ROOT / ".vela" / "tmp" / "target-index-candidate.json"
REPOSITORY_PATH = ROOT / ".vela" / "repository.json"
PACKET_PATH = ROOT / "targets" / "quantum-10-1-4.json"
CLAIM_ID = "vcl_da1b447d2c2a260ca9ca968066664ac2deee3f99b3d9e6e6f3fdb16a725bc1f8"
CLAIM_ROOT = "sha256:d02a55d6acc25c4d9908363f5f9ed4194672560d9a8da348bb60e8d44486bbbf"
CLAIM_PATH = (
    "records/claims/sha256/"
    "d02a55d6acc25c4d9908363f5f9ed4194672560d9a8da348bb60e8d44486bbbf.json"
)
WITNESS_ROOT = "sha256:f23ac24e932de13538ac842bc2a467648aa82628577cffff6c71411e59a06a3c"
VERIFIER_ROOT = "sha256:cba438b1c1e6dfafe4767ec5393573e6ae0bc387bf7995c1a423a3e50e755516"
REPORT_ROOT = "sha256:9a2282be31eef1784304ae58aa5dc00e1871fb1ba2d46c0047153c7d04e3fc35"
PROPOSED_CLAIM = (
    "The nine Pauli generators in witness "
    "sha256:f23ac24e932de13538ac842bc2a467648aa82628577cffff6c71411e59a06a3c "
    "define a ten-qubit stabilizer with rank 9 and exact logical distance 4 "
    "under exhaustive binary-symplectic centralizer reconstruction; therefore "
    "an explicit [[10,1,4]] stabilizer code exists."
)
PROPOSED_SCOPE = (
    "This establishes existence and exact parameters of this one retained "
    "stabilizer witness. It does not establish optimality at length 10, "
    "uniqueness, novelty, classification, independent-participant replication, "
    "or scientific acceptance before an authorized Decision."
)
PROPOSED_VERIFICATION = (
    "Recompute witness "
    "sha256:f23ac24e932de13538ac842bc2a467648aa82628577cffff6c71411e59a06a3c "
    "with scripts/verify_quantum_certificate.py "
    "sha256:cba438b1c1e6dfafe4767ec5393573e6ae0bc387bf7995c1a423a3e50e755516; "
    "confirm nine pairwise-commuting independent generators, encoded dimension "
    "1, a 2,048-element centralizer, 1,536 non-stabilizer logical Paulis, and "
    "exact minimum logical weight 4; and byte-match report "
    "sha256:9a2282be31eef1784304ae58aa5dc00e1871fb1ba2d46c0047153c7d04e3fc35."
)
INPUT_PATHS = [
    ".vela/repository.json",
    "artifacts/quantum-10-1-4.witness.json",
    CLAIM_PATH,
    "scripts/build_target_index.py",
    "scripts/verify_quantum_certificate.py",
    "tests/test_quantum_certificate.py",
    "tests/test_target_index.py",
    "verifiers/quantum-10-1-4-centralizer.v1.json",
]
TARGET = {
    "id": "quantum:[[10,1,4]]",
    "title": "Explicit [[10,1,4]] stabilizer code",
    "why": (
        "The accepted Claim still records existence as open, while the retained "
        "witness and exact verifier now provide bounded mechanical evidence for "
        "one explicit code."
    ),
    "state": "open",
    "rank": 1,
    "objective": (
        "Submit the exact retained witness as a bounded proposed existence Claim "
        "for independent verification and a separate authorized human Decision."
    ),
    "labels": [
        "machine-checkable",
        "quantum-code",
        "stabilizer",
        "supersede-open-question",
    ],
    "packet": {
        "path": "targets/quantum-10-1-4.json",
        "schema": "quantum-codes.stabilizer-admission-work.v1",
    },
}


def git_head() -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD^{commit}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode()


def sha256_root(path: pathlib.Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def validate_packet() -> None:
    repository = json.loads(REPOSITORY_PATH.read_text())
    packet = json.loads(PACKET_PATH.read_text())
    if set(packet) != {
        "accepted_state",
        "authority",
        "completion_contract",
        "evidence",
        "frontier_id",
        "proposed_submission",
        "repository",
        "schema",
        "target",
    }:
        raise ValueError("quantum target packet fields are not the closed admission set")
    if packet["schema"] != TARGET["packet"]["schema"]:
        raise ValueError("quantum target packet schema differs from the Target")
    if packet["frontier_id"] != repository["frontier_id"]:
        raise ValueError("quantum target packet targets another Frontier")
    if packet["repository"]["root"] != sha256_root(REPOSITORY_PATH):
        raise ValueError("quantum target packet is stale for the repository root")
    if packet["target"]["id"] != TARGET["id"] or packet["target"]["state"] != "open":
        raise ValueError("quantum target packet does not describe the open Target")

    accepted = {
        row["claim_id"]: (row["claim_root"], row["standing"])
        for row in repository["accepted_claims"]
    }
    bound_claim = packet["accepted_state"]["open_question"]
    if (
        accepted.get(bound_claim["claim_id"])
        != (bound_claim["claim_root"], bound_claim["standing"])
        or bound_claim["claim_id"] != CLAIM_ID
        or bound_claim["claim_root"] != CLAIM_ROOT
        or bound_claim["path"] != CLAIM_PATH
        or sha256_root(ROOT / CLAIM_PATH) != CLAIM_ROOT
    ):
        raise ValueError("quantum target packet does not bind the accepted open Claim")

    witness = packet["evidence"]["witness"]
    verifier = packet["evidence"]["verifier"]
    if witness["sha256"] != WITNESS_ROOT or sha256_root(ROOT / witness["path"]) != WITNESS_ROOT:
        raise ValueError("quantum target packet witness root mismatch")
    if verifier["sha256"] != VERIFIER_ROOT or sha256_root(ROOT / verifier["path"]) != VERIFIER_ROOT:
        raise ValueError("quantum target packet verifier root mismatch")
    if verifier["expected_report_sha256"] != REPORT_ROOT:
        raise ValueError("quantum target packet report root mismatch")

    proposed = packet["proposed_submission"]
    if proposed["requested_change"]["target"] != {
        "claim_id": CLAIM_ID,
        "claim_root": CLAIM_ROOT,
    }:
        raise ValueError("quantum target packet proposed change is not Claim-bound")
    if proposed["claim"] != PROPOSED_CLAIM:
        raise ValueError("quantum target packet proposed Claim text mismatch")
    if proposed["scope"] != PROPOSED_SCOPE:
        raise ValueError("quantum target packet proposed scope text mismatch")
    if proposed["verification"] != PROPOSED_VERIFICATION:
        raise ValueError("quantum target packet proposed verification text mismatch")
    if packet["authority"] != {
        "producer_ceiling": "pending_review",
        "verification_ceiling": "evidence_only",
        "accepted_standing_effect": "none",
        "requires_human_decision": True,
    }:
        raise ValueError("quantum target packet authority ceiling mismatch")


def candidate() -> dict[str, Any]:
    validate_packet()
    return {
        "schema": "vela.target-index-candidate.v1",
        "frontier_id": "vfr_001f148c07eebecb",
        "source": {
            "git_commit": git_head(),
            "input_paths": INPUT_PATHS,
        },
        "targets": [TARGET],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=CANDIDATE_PATH,
    )
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_bytes(candidate()))
    try:
        display = output.relative_to(ROOT)
    except ValueError:
        display = output
    print(f"Wrote {display}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
