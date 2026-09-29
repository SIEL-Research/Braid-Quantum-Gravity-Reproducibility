# BGCE491 scouting plan

## Question

Can BGCE490's typed canonical Halmos-Chebyshev walk be compiled from the
already realized source-word LCU unitary without constructing
`sqrt(I-H^2/alpha^2)` as a new physical primitive?

## Construction

For any source-word LCU unitary `U_A` with Hermitian success block `A`, add one
encoded signal qubit and define

`U_tilde=[[0,U_A],[U_A^dagger,0]]`.

It is a Hermitian involution.  Compressing to `|+>` on the new qubit and the
LCU success state gives exactly `A`.  Reflect about that success subspace and
form `W=S U_tilde`; the compressed powers obey the Chebyshev recurrence.

## Checks

- all eight signed sectors and all four controls;
- every distinct normalized source spectral node;
- all powers through the BGCE490 degree bound;
- three source-orientation phases to ensure dilation independence;
- unitarity, Hermiticity, involution, signal-block and Chebyshev residuals;
- retain the typed-controller versus bare-Braid boundary.
