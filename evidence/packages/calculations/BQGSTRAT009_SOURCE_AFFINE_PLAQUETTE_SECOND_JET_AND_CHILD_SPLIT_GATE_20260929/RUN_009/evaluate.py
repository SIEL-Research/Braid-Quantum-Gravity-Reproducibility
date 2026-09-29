#!/usr/bin/env python3
import hashlib
import itertools
import json
import subprocess
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def load(path):
    return json.loads((ROOT / path).read_text())


def git_json(revision, path):
    raw = subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)
    return json.loads(raw)


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def clean(poly):
    return {word: value for word, value in poly.items() if value}


def add(*polys):
    out = defaultdict(Fraction)
    for poly in polys:
        for word, value in poly.items():
            out[word] += value
    return clean(out)


def scale(poly, factor):
    return clean({word: factor * value for word, value in poly.items()})


def multiply(left, right, degree=2):
    out = defaultdict(Fraction)
    for a, av in left.items():
        for b, bv in right.items():
            word = a + b
            if len(word) <= degree:
                out[word] += av * bv
    return clean(out)


def exp2(name, sign=1):
    s = Fraction(sign)
    return {(): Fraction(1), (name,): s, (name, name): s * s / 2}


def log2(product):
    q = add(product, {(): Fraction(-1)})
    return add(q, scale(multiply(q, q), Fraction(-1, 2)))


def commutator(x, y):
    return add(multiply(x, y), scale(multiply(y, x), Fraction(-1)))


def generator(name, sign=1):
    return {(name,): Fraction(sign)}


def substitute(poly, mapping):
    out = defaultdict(Fraction)
    for word, value in poly.items():
        out[tuple(mapping.get(symbol, symbol) for symbol in word)] += value
    return clean(out)


def serialise(poly):
    return {"1" if not word else "*".join(word): str(value) for word, value in sorted(poly.items())}


sources = load(
    "records/BQGSTRAT009_SOURCE_AFFINE_PLAQUETTE_SECOND_JET_AND_CHILD_SPLIT_GATE_20260929/"
    "RUN_009/SOURCE_MATRIX.json"
)
for source in sources["sources"]:
    if "revision" in source:
        raw = subprocess.check_output(["git", "show", f"{source['revision']}:{source['path']}"], cwd=ROOT)
        assert hashlib.sha256(raw).hexdigest() == source["sha256"]
    else:
        assert digest(source["path"]) == source["sha256"]

bgce094 = load("records/BGCE094_TEMPORAL_CARTAN_PAIR_CONDITIONAL_FINITE_ACTION_PACKET_20260919/RESULT.json")
bgce097 = load("records/BGCE097_FULL_SIX_FACE_ACTION_FIVE_ADIC_ADDITIVITY_GATE_20260919/RESULT.json")
bgce137 = load("records/BGCE137_DISCRETE_S4_CHART_TRANSITION_VERSUS_NEAR_IDENTITY_CARTAN_CONNECTION_FACTORING_GATE_20260919/RESULT.json")
bgce138 = load("records/BGCE138_SOURCE_CYLINDER_DIAGONAL_LOCALIZATION_AND_MINIMAL_SMOOTH_CARTAN_COMPLETION_GATE_20260919/RESULT.json")
strat5 = git_json(
    "a8a912cb8d17c312fd171ecefa8c2cbdd17af3fc",
    "records/BQGSTRAT005_SPECTRAL_TRANSPORT_REFINEMENT_COCYCLE_GATE_20260929/BQGSTRAT_005/RESULT.json"
)
strat8 = load("records/BQGSTRAT008_ACTUAL_PALATINI_SECOND_JET_IDENTIFIABILITY_GATE_20260929/RUN_008/RESULT.json")

# Exact free-associative plaquette log through total degree two.
sequence = [("A", 1), ("B", 1), ("C", -1), ("D", -1)]
product = {(): Fraction(1)}
for name, sign in sequence:
    product = multiply(product, exp2(name, sign))
actual_log = log2(product)

linear = {}
z = []
for name, sign in sequence:
    item = generator(name, sign)
    z.append(item)
    linear = add(linear, item)
quadratic = {}
for i in range(len(z)):
    for j in range(i + 1, len(z)):
        quadratic = add(quadratic, scale(commutator(z[i], z[j]), Fraction(1, 2)))
expected_log = add(linear, quadratic)

inverse_product = {(): Fraction(1)}
for name, sign in [("D", 1), ("C", 1), ("B", -1), ("A", -1)]:
    inverse_product = multiply(inverse_product, exp2(name, sign))
inverse_log = log2(inverse_product)

constant_log = substitute(actual_log, {"C": "A", "D": "B"})
expected_constant = {("A", "B"): Fraction(1), ("B", "A"): Fraction(-1)}

plaquette_checks = {
    "general_BCH_second_jet_exact": actual_log == expected_log,
    "orientation_reversal_negates_log": inverse_log == scale(actual_log, Fraction(-1)),
    "constant_connection_linear_term_zero": all(len(word) != 1 for word in constant_log),
    "constant_connection_quadratic_is_commutator": constant_log == expected_constant
}

# Exact depth-one n=5 source four-cube incidence.
n = 5
vertices = list(itertools.product(range(n + 1), repeat=4))
boundary_vertices = [v for v in vertices if any(x in (0, n) for x in v)]
interior_vertices = [v for v in vertices if all(0 < x < n for x in v)]

edges = []
for start in vertices:
    for mu in range(4):
        if start[mu] < n:
            edges.append((start, mu))

def boundary_edge(edge):
    start, mu = edge
    return any(start[j] in (0, n) for j in range(4) if j != mu)

boundary_edges = [edge for edge in edges if boundary_edge(edge)]
interior_edges = [edge for edge in edges if not boundary_edge(edge)]

faces = []
incidence = defaultdict(int)
for mu in range(4):
    for nu in range(mu + 1, 4):
        ranges = [range(n + 1) for _ in range(4)]
        ranges[mu] = range(n)
        ranges[nu] = range(n)
        for start in itertools.product(*ranges):
            faces.append((start, mu, nu))
            start_mu = list(start)
            start_mu[mu] += 1
            start_nu = list(start)
            start_nu[nu] += 1
            incidence[(start, mu)] += 1
            incidence[(tuple(start_mu), nu)] += 1
            incidence[(tuple(start_nu), mu)] -= 1
            incidence[(start, nu)] -= 1

def boundary_face(face):
    start, mu, nu = face
    return any(start[j] in (0, n) for j in range(4) if j not in (mu, nu))

boundary_faces = [face for face in faces if boundary_face(face)]
interior_faces = [face for face in faces if not boundary_face(face)]

counts = {
    "cells": n ** 4,
    "vertices_total": len(vertices),
    "vertices_boundary": len(boundary_vertices),
    "vertices_interior": len(interior_vertices),
    "edges_total": len(edges),
    "edges_boundary": len(boundary_edges),
    "edges_interior": len(interior_edges),
    "faces_total": len(faces),
    "faces_boundary": len(boundary_faces),
    "faces_interior": len(interior_faces)
}

expected_counts = {
    "cells": 625,
    "vertices_total": 1296,
    "vertices_boundary": 1040,
    "vertices_interior": 256,
    "edges_total": 4320,
    "edges_boundary": 3040,
    "edges_interior": 1280,
    "faces_total": 5400,
    "faces_boundary": 3000,
    "faces_interior": 2400
}

interior_incidence_residuals = {str(edge): incidence[edge] for edge in interior_edges if incidence[edge] != 0}
incidence_checks = {
    "source_children_625": bgce137["derived_refinement"]["children_per_parent"] == counts["cells"] == 625,
    "all_counts_exact": counts == expected_counts,
    "all_interior_edge_linear_incidence_zero": not interior_incidence_residuals,
    "flat_face_log_zero": not log2({(): Fraction(1)})
}

raw_dimensions = {
    "coframe_components_per_vertex": 16,
    "connection_components_per_edge": 16,
    "interior_coordinates": 16 * len(interior_vertices) + 16 * len(interior_edges),
    "boundary_coordinates": 16 * len(boundary_vertices) + 16 * len(boundary_edges),
    "K_ii_shape": [16 * len(interior_vertices) + 16 * len(interior_edges)] * 2,
    "K_ib_shape": [16 * len(interior_vertices) + 16 * len(interior_edges), 16 * len(boundary_vertices) + 16 * len(boundary_edges)]
}

source_checks = {
    "Palatini_temporal_condition_preserved": bgce094["assumption_count"] == 2,
    "face_log_scaling_present": "face curvature F=O(h^2)" in bgce097["positive_result"],
    "identity_component_present": "identity component" in bgce137["graded_Cartan_factorization"]["continuous_local_connection_component"],
    "Pexp_link_discretization_present": "path-ordered" in bgce138["minimal_smooth_completion"]["connection_coarsening"],
    "flat_anchor_present": bgce138["minimal_smooth_completion"]["background"] == "e=3 I_4 and Gamma=0",
    "ordered_history_required": "ordered source history" in strat5["positive_scoped_result"],
    "prior_nonidentifiability_preserved": strat8["parent_status"] == "OPEN_SOURCE_SECOND_JET_CONSTRUCTION_REQUIRED"
}

stationarity_checks = {
    "coframe_gradient_zero_at_flat_anchor": incidence_checks["flat_face_log_zero"],
    "interior_connection_gradient_zero_by_incidence": incidence_checks["all_interior_edge_linear_incidence_zero"],
    "raw_K_blocks_well_defined": raw_dimensions["interior_coordinates"] == 24576 and raw_dimensions["boundary_coordinates"] == 65280,
    "rank_or_crossing_evaluated": False,
    "component_selection_proved": False
}

theorem = (HERE / "THEOREM.md").read_text()
out = {
    "schema": "siel.public-calculation.bqgstrat009.raw.v1",
    "source_checks": source_checks,
    "plaquette_checks": plaquette_checks,
    "plaquette_log_degree_two": serialise(actual_log),
    "constant_connection_log": serialise(constant_log),
    "incidence_counts": counts,
    "incidence_checks": incidence_checks,
    "interior_incidence_residuals": interior_incidence_residuals,
    "raw_field_dimensions": raw_dimensions,
    "stationarity_checks": stationarity_checks,
    "second_variation": "C sum epsilon epsilon [2 ebar f (D a) + ebar ebar Q(a,a)]",
    "K_blocks": {"K_ii": "H restricted to interior x interior", "K_ib": "H restricted to interior x boundary"},
    "construction_passed": all(source_checks.values()) and all(plaquette_checks.values()) and all(incidence_checks.values()) and all(value for key, value in stationarity_checks.items() if key not in ("rank_or_crossing_evaluated", "component_selection_proved")),
    "actual_caustic_closed": False,
    "theorem_sha256": hashlib.sha256(theorem.encode()).hexdigest()
}

(HERE / "RAW_OUTPUT.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps(out, indent=2, sort_keys=True))
