"""Reproduce Eq. (P1) from the eight signed crossings in Eq. (55)."""

import json
from pathlib import Path

source = json.loads(Path(__file__).with_name("crossings.json").read_text())
n = len(source["basis"]["ordered_basis"])
permutation = source["row_to_column"]
if sorted(permutation) != list(range(n * n)):
    raise ValueError("Expected a signed permutation on the two-strand basis")
if [s["mask"] for s in source["sectors"]] != [0, 5, 8, 13, 16, 21, 24, 29]:
    raise ValueError("Expected the eight masks printed in Eq. (55)")

results = []
for sector in source["sectors"]:
    negative = set(sector["negative_rows"])
    crossing = [[0] * (n * n) for _ in permutation]
    for row, col in enumerate(permutation):
        crossing[row][col] = -1 if row in negative else 1

    right_trace = [
        [sum(crossing[n*a+k][n*b+k] for k in range(n)) for b in range(n)]
        for a in range(n)
    ]
    left_trace = [
        [sum(crossing[n*k+a][n*k+b] for k in range(n)) for b in range(n)]
        for a in range(n)
    ]
    expected_trace = [[value if a == b else 0 for b in range(n)]
                      for a, value in enumerate((2, 2, 2, 2, 1))]
    if left_trace != expected_trace or right_trace != expected_trace:
        raise ValueError(f"Wrong partial traces for mask {sector['mask']}")
    gram = [[sum(right_trace[k][a] * right_trace[k][b] for k in range(n))
             for b in range(n)] for a in range(n)]
    spectrum = [gram[a][a] for a in range(n)]
    lowest = [a for a in range(n) if spectrum[a] == min(spectrum)]
    if lowest != [4]:
        raise ValueError(f"Wrong least eigenspace for mask {sector['mask']}")
    p = lowest[0]
    for a in range(n):
        for b in range(n):
            if 4 * (a == b) - gram[a][b] != 3 * (a == p and b == p):
                raise ValueError("Wrong projector polynomial")
    fixed_row = n*p + p
    if crossing[fixed_row][fixed_row] != 1:
        raise ValueError("R does not fix the recovered tensor-square line with sign +1")
    results.append({"mask": sector["mask"], "partial_trace_diagonal": [2, 2, 2, 2, 1],
                    "gram_eigenvalues_in_basis": spectrum, "recovered_basis_index": p,
                    "tensor_square_eigenvalue": crossing[fixed_row][fixed_row]})

print(json.dumps({"claim": "V120-LEM-01", "checked": results}, indent=2))
