from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "verify_quantum_certificate.py"
WITNESS = ROOT / "artifacts" / "quantum-10-1-4.witness.json"


class QuantumCertificateTests(unittest.TestCase):
    def run_verifier(self, witness: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(witness)],
            capture_output=True,
            text=True,
            timeout=30,
        )

    def write_witness(self, value: dict[str, object]) -> pathlib.Path:
        temporary = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
        )
        with temporary:
            json.dump(value, temporary)
            temporary.write("\n")
        self.addCleanup(pathlib.Path(temporary.name).unlink, missing_ok=True)
        return pathlib.Path(temporary.name)

    def test_retained_witness_reconstructs_exact_distance_four(self) -> None:
        completed = self.run_verifier(WITNESS)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(
            result,
            {
                "algorithm": "gf2_symplectic_centralizer_exhaustive_v1",
                "centralizer_dimension": 11,
                "centralizer_size": 2048,
                "encoded_dimension": 1,
                "exact_distance": 4,
                "generator_count": 9,
                "generator_rank": 9,
                "k": 1,
                "logical_weight_distribution": {
                    "4": 40,
                    "5": 72,
                    "6": 280,
                    "7": 240,
                    "8": 600,
                    "9": 200,
                    "10": 104,
                },
                "minimum_logical_examples": [
                    "IIIIIZYIXZ",
                    "IIIIXZIZIX",
                    "IIIIYXXIZI",
                    "IIIXIZXIIY",
                    "IIIYIIZYZI",
                ],
                "n": 10,
                "nonstabilizer_centralizer_size": 1536,
                "pairwise_commuting": True,
                "schema": "quantum-codes.independent-stabilizer-reconstruction.v1",
                "stabilizer_size": 512,
                "target": "quantum:[[10,1,4]]",
                "witness_sha256": (
                    "sha256:"
                    "f23ac24e932de13538ac842bc2a467648aa82628577cffff6c71411e59a06a3c"
                ),
            },
        )
        self.assertEqual(
            hashlib.sha256(completed.stdout.encode()).hexdigest(),
            "9a2282be31eef1784304ae58aa5dc00e1871fb1ba2d46c0047153c7d04e3fc35",
        )

    def test_commuting_rank_nine_distance_one_candidate_is_rejected(self) -> None:
        low_distance = {
            "schema": "canopus.quantum-stabilizer-witness.v1",
            "target": "quantum:[[10,1,4]]",
            "n": 10,
            "k": 1,
            "generators": [
                "ZIIIIIIIII",
                "IZIIIIIIII",
                "IIZIIIIIII",
                "IIIZIIIIII",
                "IIIIZIIIII",
                "IIIIIZIIII",
                "IIIIIIZIII",
                "IIIIIIIZII",
                "IIIIIIIIZI",
            ],
        }
        completed = self.run_verifier(self.write_witness(low_distance))
        self.assertEqual(completed.returncode, 1)
        self.assertIn("exact logical distance is 1", completed.stderr)

    def test_noncommuting_generators_are_rejected(self) -> None:
        witness = json.loads(WITNESS.read_text())
        witness["generators"][0] = "XIIIIIIIII"
        witness["generators"][1] = "ZIIIIIIIII"
        completed = self.run_verifier(self.write_witness(witness))
        self.assertEqual(completed.returncode, 1)
        self.assertIn("generators do not commute", completed.stderr)


if __name__ == "__main__":
    unittest.main()
