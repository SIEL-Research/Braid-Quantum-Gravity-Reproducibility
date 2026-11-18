"""Exact rational replay of the purecross example after Eq. (S7)."""

from fractions import Fraction as Q
import json

# Coordinate order (z,x,y). The smearing rho is identically one near the point.
mu, x0, y0 = Q(1, 32), Q(2, 5), Q(2, 5)
rho = Q(1)
gamma_diagonal = (1 - 2*mu*x0*y0, Q(1), Q(1))
if min(gamma_diagonal) <= 0:
    raise ValueError("The spatial metric must be positive at the test point")
grad_rho = (Q(0), Q(0), Q(0))
dx = (Q(0), Q(1), Q(0))
lapse_n = rho
lapse_m = Q(0)  # M=(x-x0)rho at the evaluation point.
grad_n = grad_rho
grad_m = tuple(rho * v for v in dx)
beta = tuple((lapse_n * grad_m[i] - lapse_m * grad_n[i]) / gamma_diagonal[i]
             for i in range(3))

# beta=rho^2 d/dx in a neighbourhood. On the plateau its derivatives vanish,
# so only the directional derivative of gamma_zz contributes to this component.
grad_gamma_zz = (Q(0), -2*mu*y0, -2*mu*x0)
lie_gamma_zz = sum(b * d for b, d in zip(beta, grad_gamma_zz))
if beta != (0, 1, 0) or lie_gamma_zz != Q(-1, 40):
    raise ValueError("The S7 nonzero shift witness differs from the paper")

print(json.dumps({"claim": "V120-THE-01", "check": "Eq. (S7) purecross witness",
                  "beta_z_x_y": [str(v) for v in beta],
                  "lie_beta_gamma_zz": str(lie_gamma_zz)}, indent=2))
