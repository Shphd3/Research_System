# Nested Common/Rare Separate-Update Mechanism

## Core intuition

Nested next-token learning does not learn all patterns in a neutral space.

A common prefix or common predictive condition is learned early and repeatedly.
Because it is useful for many examples, cross-entropy keeps rewarding larger
finite margins along this direction. The direction first aligns, then its gain
keeps growing.

Later rare or tail patterns are learned inside this already anisotropic geometry.
If the rare prediction error has nonzero projection onto the common high-gain
mode, then the local first-order update gets a cheaper loss decrease by reusing
that mode.

So the failure is not:

```text
rare information is absent.
```

The sharper failure is:

```text
rare information exists, but its update is absorbed by the common high-gain
update channel before it forms a stable discriminative path.
```

## Mechanism chain

```text
common prefix / common context appears often
-> common direction becomes stable high-gain backbone
-> common examples keep increasing margin after they are already easy
-> later rare examples reuse the high-gain common direction
-> rare discriminative residual receives too little clean update mass
-> rare loss remains high or rare route/function binding stays weak
```

## Correct intervention level

The intervention should not only change hidden states.

It should change the actual update direction:

$$
\tilde u_t = r_t (I - \rho_t P_C) u_t
$$

where:

- $u_t$: actual preconditioned update direction;
- $P_C$: frozen common-subspace projector;
- $\rho_t$: suppression strength;
- $r_t$: residual / confidence gate.

The important diagnostic is:

$$
\alpha^{C}_{tail}
=
\frac{\|P_C u_{tail}\|^2}{\|u_{tail}\|^2+\epsilon}
$$

If the mechanism is real, separate updating should reduce
$\alpha^{C}_{tail}$, improve tail / rare loss, and preserve common loss.

## What this does not claim

This does not claim:

```text
real-DCLM specialization exists;
MoE beats dense in general;
all common directions are harmful;
routing NMI proves utility;
one global common projector is enough.
```

It only tests whether common/rare separate updating is the right computational
mechanism on a controlled nested surface.
