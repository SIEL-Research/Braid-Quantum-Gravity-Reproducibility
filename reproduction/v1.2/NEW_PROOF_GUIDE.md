# New analytic and finite results in BQG v1.2

The statement identifiers and equation tags below match Appendix C.1 of the manuscript. The smooth construction uses the same classical seed action for the canonical and metric BV reductions. The finite pointing lemma concerns the specified eight signed matrices.

## Classical HDA (V120-THE-01)

Let $U$ be a contractible, globally hyperbolic four-dimensional patch with a nondegenerate oriented and time-oriented Lorentz coframe $e$. The gauge descriptors and variations have compact support in the interior away from boundaries, corners and marked lines. Work in pure gravity with zero cosmological term, $\kappa\ne0$, and a spacelike slice $\Sigma$ with positive lapse. Set $\eta=\operatorname{diag}(-1,1,1,1)$, $\epsilon_{0123}=1$, and take $F^{ab}=\frac12 F_{\mu\nu}^{ab}dx^\mu\wedge dx^\nu$.

**(S1), (S2).** The Palatini action and its contorsion decomposition are
$$
\begin{split}
 S_0[e,A]&=\frac{\kappa}{4}\int_U\epsilon_{abcd}e^a\wedge e^b\wedge F^{cd}(A),\\
 S_0[e,\omega+C]&= S_{\rm EH}[g]+\frac{\kappa}{4}\int_{\partial U}\epsilon_{abcd}e^a\wedge e^b\wedge C^{cd}
 +\frac{\kappa}{4}\int_U\epsilon_{abcd}e^a\wedge e^b\wedge C^c{}_r\wedge C^{rd},\\
 S_{\rm EH}[g]&=\frac{\kappa}{2}\int_U R[g]\,d\mathrm{vol}_g,\qquad g=e^{\mathsf T}\eta e.
\end{split}
$$
Here $\omega(e)$ is torsion free and $D_\omega(e\wedge e)=0$. Varying $C$ gives the torsion equation $\epsilon_{abcd}e^c\wedge T^d=0$, with $T^a=C^a{}_b\wedge e^b$. Dualize the internal pair to obtain $e^a\wedge T^b=e^b\wedge T^a$. Contract with the dual frame and sum over $b$: $T^a=-e^a\wedge V$, $V=\sum_b\iota_bT^b$, and $V=-3V$. The resulting $T=0$ forces $C=0$ by uniqueness of the torsion-free connection. This proves invertibility of the algebraic contorsion equation on this branch. The local Lorentz quotient leaves $g$.

**(S3).** In time gauge on $\Sigma$, write $r_i^a$ for the spatial triad, $E_a^i=\sqrt\gamma\,r_a^i$ for the densitized inverse, and $K_{ij}=k_i^a r_{ja}$ for the symmetric tensor obtained from the boost connection. The Palatini potential is $\kappa\int_\Sigma E_a^i\delta k_i^a$. Using $k_i^a\delta E_a^i=\frac12\sqrt\gamma(K\gamma^{ij}-K^{ij})\delta\gamma_{ij}$ gives
$$
 \Theta_{\rm P}=\delta\left(\kappa\int_\Sigma\sqrt\gamma K\right)
 +\int_\Sigma\pi^{ij}\delta\gamma_{ij},\qquad
 \pi^{ij}=\frac{\kappa\sqrt\gamma}{2}(K^{ij}-K\gamma^{ij}).
$$
The Gauss charge vanishes on reduction. The supported spatial divergence contributes zero. The exact field variation contributes zero to $\Omega=\int_\Sigma\delta\gamma_{ij}\wedge\delta\pi^{ij}$.

**(S4).** The $3+1$ bulk Lagrangian density is $\frac{\kappa}{2}\alpha\sqrt\gamma (R_\gamma+K_{ij}K^{ij}-K^2)$, with $K_{ij}=(\dot\gamma_{ij}-\mathcal L_w\gamma_{ij})/(2\alpha)$. Its Legendre derivative is (S3). The canonical generators on $(\gamma,\pi)$ are
$$
 H[N]=\int_\Sigma N\left[
 \frac{2}{\kappa\sqrt\gamma}\left(\pi^{ij}\pi_{ij}-\frac{\pi^2}{2}\right)
 -\frac{\kappa}{2}\sqrt\gamma R_\gamma\right],\qquad
 D[W]=\int_\Sigma \pi^{ij}(\mathcal L_W\gamma)_{ij}
 =\int_\Sigma W^i\mathcal D_i ,
 \qquad \mathcal D_i=-2\gamma_{ik}\nabla_j\pi^{jk}.
$$
Here $\pi=\gamma_{ij}\pi^{ij}$. The lapse and shift have vanishing primary momenta.

**(S5), (S6).** Use $\{F,G\}=\int_\Sigma(F_\gamma G_\pi-F_\pi G_\gamma)$ and $X_F f=\{f,F\}$. For fixed $W$, $D_\pi=\mathcal L_W\gamma$, $D_\gamma=-\mathcal L_W\pi$ with $\pi$ a weight-one density. The Lie commutator gives $\{D[W],D[V]\}=D[[W,V]]$. The Lie derivative on the Hamiltonian density and supported integration by parts give $\{D[W],H[N]\}=H[W^i\partial_iN]$.

For $P_{ij}=\pi_{ij}-\frac12\pi\gamma_{ij}$ the contributing derivatives are
$$
 H[N]_{\pi}=\frac{4N}{\kappa\sqrt\gamma}P_{ij},\qquad
 H[N]_{\gamma}\big|_{\partial N}
 =-\frac{\kappa\sqrt\gamma}{2}(\nabla^i\nabla^jN-\gamma^{ij}\nabla^2N).
$$
Antisymmetrization removes terms proportional to $NM$. The trace adjustment cancels using $\gamma^{ij}P_{ij}=-\pi/2$. Integrating the resulting $2\pi^{ij}(N\nabla_i\nabla_jM-M\nabla_i\nabla_jN)$ by parts gives
$$
 \{H[N],H[M]\}=D[\beta],\qquad
 \beta^i=\gamma^{ij}(N\partial_jM-M\partial_jN).
$$
This is the metric-dependent identity before restriction to the constraint surface. See [Teitelboim (1973)](https://doi.org/10.1016/0003-4916(73)90096-1).

**(S7).** The variation of $D[\beta]$ includes $\mathcal D_i\delta\beta^i$, with $\delta\beta^i=-\gamma^{i(a}\beta^{b)}\delta\gamma_{ab}$. Thus $X_{D[\beta]}\gamma=\mathcal L_\beta\gamma$ and $X_{D[\beta]}\pi^{ab}=(\mathcal L_\beta\pi)^{ab}+\mathcal D_i\gamma^{i(a}\beta^{b)}$. The off-shell term is part of the generator. [The rational example](verify_hda_example.py) replays the purecross shift and metric variation at the stated point.

## Local perturbative QME (V120-THE-02)

**(S8).** For the diffeomorphism ghost $c$ and Lorentz ghost $\ell$ use $qe=\mathcal L_c e+\ell e$, $qA=\mathcal L_c A-D_A\ell$, $qc=c^\mu\partial_\mu c$, and $q\ell=\mathcal L_c\ell+\frac12[\ell,\ell]_{\rm gr}$. The graded Jacobi and compatibility identities give $q^2=0$, including the mixed terms. On the declared support, invariance gives $qS_0=0$. The BV cotangent lift then obeys the classical master equation. The lift of $C=A-\omega(e)$ is canonical and $qC$ is homogeneous in $C$. At $C^*=0$ its algebraic equation eliminates the pair $C,C^*$. A local Lorentz coordinate and its BRST variation give a contractible pair. The metric action is
$$
 S_{\rm BV}^{g}=S_{\rm EH}[g]+\int_U g^{*\mu\nu}(\mathcal L_c g)_{\mu\nu}
  -\int_U c^*_\mu c^\nu\partial_\nu c^\mu,\qquad (S_{\rm BV}^g,S_{\rm BV}^g)=0 .
$$
The antifields are densities. The metric is the same $g$ as in (S2). On the slice the normal and tangential descriptors are related by $c^\perp=\alpha c^t$, $c_\parallel^i=c^i+w^ic^t$. The metric BV construction includes the lapse and shift variables.

**(S9), (S10).** Expand about a smooth vacuum background, keep fluctuations off shell, and use de Donder gauge with the nonminimal doublet. The free metric and ghost system is normally hyperbolic after trace reversal for the metric. Work with local covariant causal renormalization and the allowed local effective field theory counterterms. Write the renormalized Ward defect as $\mathfrak Q_{\mathcal T}(W)=\tfrac12(W,W)-\mathcal A_{\mathcal T}(W)$ with $\mathcal A_{\mathcal T}=O(\hbar)$. At its first nonzero order $\hbar^L$, Ward consistency gives $s a_L=0\bmod d$ for the local defect density $a_L$. The pure four-dimensional metric anomaly cohomology $H^{1,4}(s\mid d)$ vanishes in this class, with antifields included. Hence $a_L=s b_L+d c_L$. Adding the correction $-\hbar^L\int b_L$ raises the order of the defect. For a cutoff equal to one near the support the divergence gives no interior contribution. Formal induction gives $W=(S_{\rm BV}^g)^\Psi+O(\hbar)$ and $\mathfrak Q_{\mathcal T}(W)=0\bmod d$. See [the proof route with primary reference locations](QME_PROOF_ROUTE.md).

The effective theory uses reduced metric quantization. The map from the original stationary refinement and physical projection to these canonical generators and the selected Braid measure remains open. Quantization prior to reduction also involves the contorsion determinant and Lorentz frame Jacobian.

## Pointing line (V120-LEM-01)

For the eight signed permutation matrices $R^{(s)}$ of [Eq. (55)](crossings.json), compute $A_s=\operatorname{Tr}_2 R^{(s)}$. The rows preserving the second index within the five first-index blocks are $\{0,2\},\{6,8\},\{10,12\},\{16,18\},\{24\}$. They are fixed rows with sign $+1$ in all eight sectors. For the other partial trace the row sets are $\{0,10\},\{6,16\},\{2,12\},\{8,18\},\{24\}$. Thus both traces are diagonal with entries $(2,2,2,2,1)$. The simple least eigenspace of $A_s^\dagger A_s$ then gives (P1):
$$
 P_{\rm pt}=\tfrac13(4I_5-A_s^\dagger A_s)=|e_4\rangle\langle e_4|.
$$
The fixed positive row 24 implies $R^{(s)}(p\otimes p)=p\otimes p$ for every unit representative $p$ of that line. The spectral rule determines the reference line within the specified tensor representation and has the same output in every signed sector. See [the integer replay](verify_pointing.py) and [Conti–Lechner, Theorem 5.8](https://doi.org/10.1112/jlms.12387).
