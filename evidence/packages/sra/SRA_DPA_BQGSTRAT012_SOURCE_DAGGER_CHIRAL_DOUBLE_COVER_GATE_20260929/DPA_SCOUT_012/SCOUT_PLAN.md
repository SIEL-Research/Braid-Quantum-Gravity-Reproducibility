# DPA-SCOUT-BQGSTRAT-012 plan

## Parent question

Does the source orientation/dagger structure define two inequivalent internal
bivector sheets whose coefficient-free real completion is not proportional to
the existing Palatini Hessian?

## Frozen sources and type rule

- Research revision: `83a71126a71fbd613c5fc1d5c493271286de9e7f`.
- `BGCE027`: the Lorentz metric and ordered tetrad orientation determine the
  internal Hodge operator on Lorentz bivectors.
- `BGCE041`: this Hodge operator acts inside the Lorentz carrier.
- `BQGQBV-002` at commit `0204a73d73cbe2e728e6a37bd11f8bf3e72cbac0`:
  the pointed Hodge-polar operator acts on the source-cell cochain factor and
  commutes with the independently derived internal coefficient module.
- `BQGSTRAT-010/011`: exact old rank profile and scalar-completion no-go.

The cochain degree-parity operator must not be identified with the internal
Lorentz Hodge operator merely because both constructions contain an
80-dimensional rank statement.

## Frozen bold hypothesis and ordinary alternative

**Bold hypothesis.**  The source orientation double cover acts on the
self-dual and anti-self-dual Lorentz-bivector representations.  Dagger swaps
the two, and its equal-weight real completion supplies a new quadratic form
without a fitted coefficient.

**Strongest ordinary alternative.**  The real Palatini action already is the
equal-weight completion of the two dagger-conjugate chiral pieces.  Their sum
reconstructs the old action exactly.  The only independent real partner is the
Holst contraction, whose relative coefficient is not selected by dagger or by
the separately typed cochain polar sign.

## Exact decision rule

Let `J` be the Lorentz Hodge operator on bivectors, so `J^2=-I`, and define

`P_+=(I-iJ)/2`, `P_-=(I+iJ)/2`.

The evaluator must establish exactly:

1. `P_+ + P_-=I`, `P_+P_-=0`, `conj(P_+)=P_-`;
2. for the Palatini insertion `J`, the two chiral insertions are `J P_+`
   and `J P_-`;
3. equal dagger weights give `J(P_++P_-)=J`, hence precisely the old action;
4. the independent combination is the Holst insertion `I`;
5. a general dagger-real coefficient pair gives `a J-b I`, leaving an
   undetermined real relative coefficient unless another typed source law
   fixes it.

PASS requires a source-fixed nonproportional real insertion.  If equal weights
return `J` and every nonproportional insertion has an unselected coefficient,
the proposed dagger/chiral repair is a scoped NO-GO.  Do not scan the
coefficient and do not rerun all 625 sectors when proportionality already
decides the gate.

## Counter-intuition and falsifier

The ordinary parity/chiral decomposition of a Lorentzian Palatini action is
not Braid-specific.  The exact falsifier is a typed source morphism coupling
the cochain polar line to internal bivector chirality and fixing a nonzero
relative Holst phase before any rank is inspected.

## Retention and claim ceiling

Retain the plan, source matrix, exact evaluator, raw output, result, verifier,
attempt ledger and report.  The scout can exclude only the declared
equal-weight dagger/chiral completion.  It cannot exclude a source-perfect
quasi-local Schur complement, a newly derived phase law, matter-induced
completion, singular/global continuation or empirical gravity.

