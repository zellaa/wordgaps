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

## Command Line Interface (CLI) Usage

The project is structured as a Python module runnable via the `wordgaps` command using `uv`. 

Needs uv, fzf, and jq to run.

### 1. Dictionary Scanning & Analysis

#### Find Longest Words
Find the longest outbound and inbound words in the dictionary:
```bash
uv run wordgaps --find-longest
```

#### Generate Valid Words JSON Database
Analyze all words in the dictionary, group them by length and category, and output to `dict/valid_words.json`:
```bash
uv run wordgaps --generate-valid
```

---

### 2. Trajectory & Distribution Plotting

#### Visualize a Single Word
Generate the trajectory and envelope width plot for a specific word (saved to `output-images/{word}.png` and opened automatically):
```bash
uv run wordgaps --plot <word>
```

#### Plot Envelope Width Distributions
Visualize the envelope width curves for all valid words of a specific length $N$. You must specify whether to plot outbound, inbound, or both (both outputs a two-panel vertical subplot, saved to `output-images/dist_{N}_{mode}.png` and opened automatically):
```bash
# Plot outbound distributions for length 5
uv run wordgaps --plot-dist 5 --outbound

# Plot inbound distributions for length 5
uv run wordgaps --plot-dist 5 --inbound

# Plot both distributions in a shared x-axis chart
uv run wordgaps --plot-dist 5 --both
```

#### Plot Counts Distribution by Length
Generate a grouped bar chart showing the count of valid outbound and inbound words for each word length in the database (saved to `output-images/word_counts_by_length.png` and opened automatically):
```bash
uv run wordgaps --plot-counts
```

---

### 3. Word Count Utility Script

A bash script is provided in `count_words.sh` to query the number of valid inbound and outbound words for a given word length.

Run the script by providing the word length as an argument (or it will prompt you if left empty):
```bash
./scripts/count_words.sh 5
```
