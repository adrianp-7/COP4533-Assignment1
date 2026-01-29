# Stable Matching Assignment

## Students
Adrian Pelaez

Arnav Bagmar

-  UFIDs submitted as comment on Canvas

## How to Run

### Matcher
python3 src/matcher.py < data/example.in > data/example.out

### Verifier
python3 src/verifier.py < data/example.in > data/example.out

## Task C
Graphs are located in graphs/.

Running python3 src/generate_inputs.py populates data/large_n with random valid preference lists.

### Observed Trend
Both the matcher and verifier exhibit O(n^2) runtime growth. Doubling n roughly quadruples runtime, consistent with the theoretical complexity of Gale–Shapley.

The graphs show that runtime increases slowly for small n  and grows rapidly as n doubles, doubling n roughly quadruples runtime.
The matcher and verifier curves are similar, with the matcher slightly slower due to more operations per proposal

## Assumptions
- Input format follows the specification.
- All preference lists are complete permutations.
- Python 3.8+ required.
