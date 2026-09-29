# BGCE443 Revision 5 closability bridge

## Standard finite-range route for the later focal evaluator

For a quasi-local spin algebra with finite-dimensional local algebras, a uniformly bounded,
self-adjoint finite-range interaction defines finite-volume Hamiltonian evolutions. The
Lieb-Robinson/thermodynamic-limit construction gives a strongly continuous one-parameter group of
star automorphisms when the corresponding interaction-norm hypotheses hold. Its closed generator
extends the derivation defined on the dense algebraic local core, so that local-core derivation is
closable.

The literature anchor used only for this theorem route is Bruno Nachtergaele and Robert Sims,
"On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian",
arXiv:1410.8174, which explicitly addresses Lieb-Robinson bounds and existence of thermodynamic-
limit dynamics. The BGCE443 focal evaluator must still instantiate, not assume:

1. self-adjointness of every transported `h_a`;
2. exact finite range `R=3`;
3. a uniform exact local norm bound;
4. word-independent transport and translation covariance;
5. the finite overlap/interaction-norm bound required by the limit theorem; and
6. agreement of the group generator with the stabilized local derivation.

No analytic convergence constant or factorial estimate is hard-coded in Revision 5.

## Stronger explicit proof for the non-focal toy

For each Pauli seed `h`, the Revision 5 constructor checks `h*=h`, `h^2=I`, translation covariance
under the explicit unsigned swaps and pairwise commutation of translated one-site terms. Therefore

`exp(i t h)=cos(t) I + i sin(t) h`

and every finite-volume evolution factorizes into commuting one-site adjoint actions. On a fixed
local observable, additional factors outside its support act trivially, so the evolution is
eventually independent of volume. The exact factorization supplies the group law, star preservation,
isometry and a closed automorphism-group generator extending the toy local derivation. This is the
actual Revision 5 toy closability certificate; the literature theorem is not used as a Boolean flag.

For the non-self-adjoint control `R`, the constructor detects both failure of self-adjoint
involution and a nonzero star-derivation defect on an explicit matrix unit, so the same endpoint
rejects it.
