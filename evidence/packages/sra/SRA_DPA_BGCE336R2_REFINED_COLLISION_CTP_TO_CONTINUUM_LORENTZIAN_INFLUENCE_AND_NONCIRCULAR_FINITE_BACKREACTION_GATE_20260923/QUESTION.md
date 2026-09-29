# BGCE336R2 question

For the same finite pointed-Braid collision source, let the refinement mesh be
`h_m=5^(-m)` and the collision contraction be
`q_m=exp(-gamma h_m)` with arbitrary `gamma>0`.

Does the refined finite CTP process converge, without first selecting a
numerical parent rate, to a normalized causal real-time continuum influence
functional with positive noise and a finite four-component total-balance
density? If so, does that continuum functional also supply a source-native
doubled-metric variation whose interaction stress closes the existing
noncircular finite Einstein backreaction?

The first fail for the second part is the absence of a source-derived map from
the doubled metric to the collision generator, nonuniqueness of the microscopic
interaction split, or reliance on the target Einstein equation to define the
stress.

Revision note: BGCE336 stopped before result construction because an auxiliary
floating-point repeated-power witness used a stage-independent tolerance.
BGCE336R1 then stopped before result writing because a Python result dictionary
used the JSON literal `false`. BGCE336R2 preserves the same scientific gate,
keeps the explicit operation-count-dependent roundoff bound, and changes only
that literal to Python `False`.
