# BGCE448 actual UB612 U4 / 55-column audit

## 結論

**SCOPED PASS / OPEN。** actual UB612 `U4_total`の35 quartic slotsに対し、
BGCE290/BGCE447の十個のsource-fixed symmetric metric directionsから55 unordered pairの
二次osculating responseを構成した。

保存intervalのexact midpointでは、35×55行列は三つの独立な素数すべてでrank 35だった。
従ってBGCE444の10→35 capacityは、抽象次元だけでなくactual U4 midpoint上にも実現する。

## 未閉鎖点

rank 35の最後のmodeは非常に細い。row-normalized screenでは二番目に小さいsingular valueは
約`4.63e-2`だが、最後は約`2.74e-16`。一方、保存intervalを独立boxとして伝播した
error norm上界は約`9.27e-4`である。このboxだけでは最後のmodeを0から分離できない。

固定した34×34 minorはBeeck screen約`2.98e-2 < 1`で安定だが、これはfloat diagnosticであり
directed-rounding endpointではない。従ってactual correlated intervalのrank 35をPASSとはしない。

## Counter-intuition scan

midpoint rank 35をactual全boxのrank 35へ昇格してはいけない。保存係数intervalは共通の
curvature backendから来るため本来は相関しているが、JSON packetではその相関が落ちている。
逆に、独立box screenが最後のmodeを認証できないことはrank 35の反証でもない。

## 次

BGCE449ではUB612 evaluatorを共通interval backendのまま再生し、選択35×35 minorまたは
同値なrank certificateへ相関を保持して流す。そこで0分離できればrank 35を閉じ、できなければ
actual packetの精度・対称性境界をNO-GOとして固定する。

本gateはfull metric Frechet Hessianではなく、same-carrier frameの二次osculating responseである。
full sigma6、parallel operator、非多項式625-child sampling、物理的UV completionは主張しない。
