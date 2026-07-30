#!/usr/bin/env python3
"""Focused tests for the one-target quantum Target Index candidate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts" / "build_target_index.py"
PACKET = ROOT / "targets" / "quantum-10-1-4.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("build_target_index", GENERATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TargetIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()

    def test_candidate_is_exact_closed_and_deterministic(self) -> None:
        first = self.generator.canonical_bytes(self.generator.candidate())
        second = self.generator.canonical_bytes(self.generator.candidate())
        self.assertEqual(first, second)
        value = json.loads(first)
        self.assertEqual(
            set(value), {"frontier_id", "schema", "source", "targets"}
        )
        self.assertEqual(value["schema"], "vela.target-index-candidate.v1")
        self.assertEqual(value["frontier_id"], "vfr_001f148c07eebecb")
        self.assertEqual(value["source"]["input_paths"], sorted(value["source"]["input_paths"]))
        self.assertNotIn(
            "targets/quantum-10-1-4.json",
            value["source"]["input_paths"],
        )
        self.assertEqual(len(value["targets"]), 1)
        self.assertEqual(value["targets"][0]["id"], "quantum:[[10,1,4]]")
        self.assertEqual(value["targets"][0]["rank"], 1)
        self.assertEqual(
            value["targets"][0]["packet"],
            {
                "path": "targets/quantum-10-1-4.json",
                "schema": "quantum-codes.stabilizer-admission-work.v1",
            },
        )

    def test_cli_output_is_byte_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = pathlib.Path(directory) / "first.json"
            second = pathlib.Path(directory) / "second.json"
            for output in (first, second):
                subprocess.run(
                    ["python3", str(GENERATOR), "--output", str(output)],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                )
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_packet_binds_exact_current_claim_and_evidence_roots(self) -> None:
        packet = json.loads(PACKET.read_text())
        claim = packet["accepted_state"]["open_question"]
        self.assertEqual(
            claim["claim_id"],
            "vcl_da1b447d2c2a260ca9ca968066664ac2deee3f99b3d9e6e6f3fdb16a725bc1f8",
        )
        for binding in (
            claim,
            packet["evidence"]["witness"],
            packet["evidence"]["verifier"],
        ):
            digest = "sha256:" + hashlib.sha256(
                (ROOT / binding["path"]).read_bytes()
            ).hexdigest()
            self.assertEqual(binding.get("claim_root", binding.get("sha256")), digest)
        self.assertEqual(
            packet["authority"],
            {
                "accepted_standing_effect": "none",
                "producer_ceiling": "pending_review",
                "requires_human_decision": True,
                "verification_ceiling": "evidence_only",
            },
        )
        self.assertEqual(
            packet["proposed_submission"]["claim"],
            self.generator.PROPOSED_CLAIM,
        )
        self.assertEqual(
            packet["proposed_submission"]["scope"],
            self.generator.PROPOSED_SCOPE,
        )
        self.assertEqual(
            packet["proposed_submission"]["verification"],
            self.generator.PROPOSED_VERIFICATION,
        )

    def test_generator_rejects_tampered_packet(self) -> None:
        original = PACKET.read_bytes()
        packet = json.loads(original)
        packet["authority"]["requires_human_decision"] = False
        try:
            PACKET.write_text(json.dumps(packet))
            with self.assertRaisesRegex(ValueError, "authority ceiling mismatch"):
                self.generator.validate_packet()
        finally:
            PACKET.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
