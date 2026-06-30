# Outbound and Inbound Words


## Mathematical Formulation

Let a word $w$ of length $n$ be represented as a sequence of character values:

```math
v = [v_1, v_2, \dots, v_n]
```

where each $v_i \in \{1, 2, \dots, 26\}$ represents the alphabetical position of character $c_i$ (e.g., $\text{A} = 1, \text{B} = 2, \dots, \text{Z} = 26$).

---

## Outbound Words

### Definition
A word is **outbound** (or $n$-outbound) if every letter in the word is either strictly before or strictly after all the letters that precede it. 

### Mathematical Formulation
In other words, for all prefix strings of length $k \in \{2, \dots, n\}$:

```math
v_k < \min_{1 \le j < k} \{v_j\} \quad \text{or} \quad v_k > \max_{1 \le j < k} \{v_j\}
```

### Envelope Width Formulation
Define the running minimum and maximum of the prefix of length $k$ (for $1 \le k \le n$) as:

```math
v^{\min}_k = \min_{1 \le j \le k} \{v_j\} \quad \text{and} \quad v^{\max}_k = \max_{1 \le j \le k} \{v_j\}
```
The **prefix width** at step $k$ is:

```math
W^{\text{out}}_k = v^{\max}_k - v^{\min}_k
```
A word is outbound if and only if the prefix width sequence is strictly increasing:

```math
W^{\text{out}}_k > W^{\text{out}}_{k-1} \quad \forall k \in \{2, \dots, n\}
```

### Examples
* **`car`** ($v = [3, 1, 18]$): **Outbound**
  * $k=1$: Initial state.
  * $k=2$: $\text{A}\ (1) < 3$, new range $[1, 3]$.
  * $k=3$: $\text{R}\ (18) > 3$, new range $[1, 18]$.
* **`app`** ($v = [1, 16, 16]$): **Not Outbound**
  * $k=3$: The second $\text{P}\ (16)$ is not strictly greater than the first $\text{P}\ (16)$.
* **`pink`** ($v = [16, 9, 14, 11]$): **Not Outbound**
  * $k=3$: $\text{N}\ (14)$ lies within the previous range of $[9, 16]$ (between $\text{I}$ and $\text{P}$).

---

## Inbound Words

### Definition
A word of length $n$ is **inbound** (or $n$-inbound) if every letter in the word is either strictly before or strictly after all the letters that follow it. 

### Mathematical Formulation
In other words, for all suffix strings starting at index $k \in \{1, \dots, n-1\}$:

```math
v_k < \min_{k < j \le n} \{v_j\} \quad \text{or} \quad v_k > \max_{k < j \le n} \{v_j\}
```
Equivalently, a word $w$ is inbound if and only if its reversed sequence $w^R$ is outbound:

```math
\text{inbound}(w) \iff \text{outbound}(w^R)
```

### Envelope Width Formulation
Define the running minimum and maximum of the suffix starting at index $k$ (for $1 \le k \le n$) as:

```math
v^{\min, \text{sfx}}_k = \min_{k \le j \le n} \{v_j\} \quad \text{and} \quad v^{\max, \text{sfx}}_k = \max_{k \le j \le n} \{v_j\}
```
The **suffix width** at step $k$ is:

```math
W^{\text{in}}_k = v^{\max, \text{sfx}}_k - v^{\min, \text{sfx}}_k
```
A word is inbound if and only if the suffix width sequence is strictly decreasing:

```math
W^{\text{in}}_{k-1} > W^{\text{in}}_k \quad \forall k \in \{2, \dots, n\}
```
