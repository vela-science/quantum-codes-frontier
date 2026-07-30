#!/usr/bin/env python3
"""Independently reconstruct the retained [[10,1,4]] certificate.

The historical Canopus capsule checked all Pauli errors of weight at most
three. This verifier uses a different calculation: it derives the complete
binary-symplectic centralizer, enumerates every logical Pauli coset
representative, and computes the exact minimum logical weight.

The result is mechanical evidence only. It does not create a Vela
Verification Record or change scientific Standing.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from typing import Any

SCHEMA = "canopus.quantum-stabilizer-witness.v1"
TARGET = "quantum:[[10,1,4]]"
N = 10
K = 1
MINIMUM_DISTANCE = 4
MAX_WITNESS_BYTES = 65_536
EXPECTED_FIELDS = {"schema", "target", "n", "k", "generators"}


class CertificateError(ValueError):
    """The retained witness does not satisfy the exact certificate contract."""


def read_witness(path: pathlib.Path) -> tuple[dict[str, Any], bytes]:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise CertificateError(f"cannot inspect witness: {error}") from error
    if path.is_symlink() or not path.is_file():
        raise CertificateError("witness must be one regular, non-symlink file")
    if metadata.st_size > MAX_WITNESS_BYTES:
        raise CertificateError(f"witness exceeds {MAX_WITNESS_BYTES} bytes")
    try:
        raw = path.read_bytes()
        witness = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CertificateError(f"witness is not valid UTF-8 JSON: {error}") from error
    if not isinstance(witness, dict) or set(witness) != EXPECTED_FIELDS:
        raise CertificateError(
            "witness fields must be exactly schema, target, n, k, generators"
        )
    return witness, raw


def pauli_vector(pauli: str, n: int) -> int:
    if len(pauli) != n or any(symbol not in "IXYZ" for symbol in pauli):
        raise CertificateError(
            f"each generator must be a length-{n} string over I, X, Y, Z"
        )
    x = 0
    z = 0
    for qubit, symbol in enumerate(pauli):
        if symbol in "XY":
            x |= 1 << qubit
        if symbol in "ZY":
            z |= 1 << qubit
    return x | (z << n)


def symplectic(left: int, right: int, n: int) -> int:
    mask = (1 << n) - 1
    left_x, left_z = left & mask, left >> n
    right_x, right_z = right & mask, right >> n
    return (
        (left_x & right_z).bit_count() + (left_z & right_x).bit_count()
    ) & 1


def reduced_basis(rows: list[int], width: int) -> tuple[list[int], list[int]]:
    basis = [row for row in rows if row]
    pivots: list[int] = []
    pivot_row = 0
    for column in range(width):
        selected = next(
            (
                row
                for row in range(pivot_row, len(basis))
                if (basis[row] >> column) & 1
            ),
            None,
        )
        if selected is None:
            continue
        basis[pivot_row], basis[selected] = basis[selected], basis[pivot_row]
        pivot = basis[pivot_row]
        for row in range(len(basis)):
            if row != pivot_row and (basis[row] >> column) & 1:
                basis[row] ^= pivot
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(basis):
            break
    return basis, pivots


def binary_span(basis: list[int]) -> set[int]:
    values = {0}
    for row in basis:
        values.update(value ^ row for value in tuple(values))
    return values


def centralizer_basis(generators: list[int], n: int) -> list[int]:
    mask = (1 << n) - 1
    constraints = []
    for generator in generators:
        generator_x = generator & mask
        generator_z = generator >> n
        constraints.append(generator_z | (generator_x << n))
    rows, pivots = reduced_basis(constraints, 2 * n)
    free_columns = [column for column in range(2 * n) if column not in pivots]
    nullspace: list[int] = []
    for free in free_columns:
        value = 1 << free
        for row, pivot in zip(rows, pivots, strict=True):
            if ((row & ~(1 << pivot)) & value).bit_count() & 1:
                value |= 1 << pivot
        if any((constraint & value).bit_count() & 1 for constraint in constraints):
            raise CertificateError("internal centralizer reconstruction failed")
        nullspace.append(value)
    return nullspace


def pauli_string(vector: int, n: int) -> str:
    mask = (1 << n) - 1
    x = vector & mask
    z = vector >> n
    symbols = []
    for qubit in range(n):
        has_x = (x >> qubit) & 1
        has_z = (z >> qubit) & 1
        symbols.append(
            "Y" if has_x and has_z else "X" if has_x else "Z" if has_z else "I"
        )
    return "".join(symbols)


def pauli_weight(vector: int, n: int) -> int:
    mask = (1 << n) - 1
    return ((vector & mask) | (vector >> n)).bit_count()


def verify(path: pathlib.Path) -> dict[str, Any]:
    witness, raw = read_witness(path)
    if witness["schema"] != SCHEMA or witness["target"] != TARGET:
        raise CertificateError("witness schema or target is wrong")
    if type(witness["n"]) is not int or type(witness["k"]) is not int:
        raise CertificateError("n and k must be integers")
    if witness["n"] != N or witness["k"] != K:
        raise CertificateError(f"witness must declare n={N} and k={K}")

    declared = witness["generators"]
    if not isinstance(declared, list) or len(declared) != N - K:
        raise CertificateError("witness must contain exactly nine generators")
    if any(not isinstance(generator, str) for generator in declared):
        raise CertificateError("every generator must be a string")
    if len(set(declared)) != len(declared):
        raise CertificateError("generators must be distinct")

    generators = [pauli_vector(generator, N) for generator in declared]
    if any(generator == 0 for generator in generators):
        raise CertificateError("identity is not a generator")
    for left_index, left in enumerate(generators):
        for right in generators[left_index + 1 :]:
            if symplectic(left, right, N):
                raise CertificateError("generators do not commute")

    stabilizer_basis, generator_pivots = reduced_basis(generators, 2 * N)
    rank = len(generator_pivots)
    if rank != N - K:
        raise CertificateError(f"generator rank is {rank}, expected {N - K}")
    stabilizer = binary_span(stabilizer_basis)
    if len(stabilizer) != 1 << (N - K):
        raise CertificateError("stabilizer span has the wrong cardinality")

    centralizer_generators = centralizer_basis(generators, N)
    expected_centralizer_dimension = N + K
    if len(centralizer_generators) != expected_centralizer_dimension:
        raise CertificateError(
            "centralizer dimension is "
            f"{len(centralizer_generators)}, expected {expected_centralizer_dimension}"
        )
    centralizer = binary_span(centralizer_generators)
    if not stabilizer <= centralizer:
        raise CertificateError("stabilizer is not contained in its centralizer")

    logical = centralizer - stabilizer
    if not logical:
        raise CertificateError("centralizer contains no non-stabilizer logical Pauli")
    distance = min(pauli_weight(vector, N) for vector in logical)
    if distance != MINIMUM_DISTANCE:
        raise CertificateError(
            f"exact logical distance is {distance}, expected {MINIMUM_DISTANCE}"
        )

    distribution: dict[str, int] = {}
    minimum_examples = []
    for vector in sorted(logical):
        weight = pauli_weight(vector, N)
        key = str(weight)
        distribution[key] = distribution.get(key, 0) + 1
        if weight == distance:
            minimum_examples.append(pauli_string(vector, N))

    return {
        "algorithm": "gf2_symplectic_centralizer_exhaustive_v1",
        "centralizer_dimension": len(centralizer_generators),
        "centralizer_size": len(centralizer),
        "encoded_dimension": N - rank,
        "exact_distance": distance,
        "generator_count": len(generators),
        "generator_rank": rank,
        "k": K,
        "logical_weight_distribution": distribution,
        "minimum_logical_examples": sorted(minimum_examples)[:5],
        "n": N,
        "nonstabilizer_centralizer_size": len(logical),
        "pairwise_commuting": True,
        "schema": "quantum-codes.independent-stabilizer-reconstruction.v1",
        "stabilizer_size": len(stabilizer),
        "target": TARGET,
        "witness_sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
    }


def canonical_bytes(value: dict[str, Any]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode()


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: verify_quantum_certificate.py WITNESS.json",
            file=sys.stderr,
        )
        return 2
    try:
        result = verify(pathlib.Path(sys.argv[1]))
    except CertificateError as error:
        print(f"quantum reconstruction: {error}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonical_bytes(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
