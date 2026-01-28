import sys
from collections import deque


def read_input():
    data = sys.stdin.read().strip().splitlines()
    if not data:  # Empty file
        return 0, [], []

    try:
        n = int(data[0].strip())
    except ValueError:
        sys.stderr.write("Invalid input: first line must be an integer n.\n")
        sys.exit(1)

    if n < 0:
        sys.stderr.write("Invalid input: n must be a positive integer.\n")
        sys.exit(1)

    if n == 0:  # No hospitals/students
        return 0, [], []

    if len(data) < 1 + 2 * n:
        sys.stderr.write("Invalid input: not enough preference lines.\n")
        sys.exit(1)

    hospital_prefs = []
    student_prefs = []

    # Traverse hospital preference lists
    for i in range(1, 1 + n):
        line = data[i].strip()

        if not line:
            sys.stderr.write(f"Invalid input: empty hospital preference line {i}.\n")
            sys.exit(1)

        try:
            prefs = list(map(int, line.split()))
        except ValueError:
            sys.stderr.write(f"Invalid input: non-integer in hospital preference line {i}.\n")
            sys.exit(1)

        if len(prefs) != n:
            sys.stderr.write(f"Invalid input: hospital {i} preference list must have {n} entries.\n")
            sys.exit(1)

        if sorted(prefs) != list(range(1, n + 1)):
            sys.stderr.write(f"Invalid input: hospital {i} preference list must be a permutation of 1..{n}.\n")
            sys.exit(1)

        # Convert to 0-based indices
        hospital_prefs.append([s - 1 for s in prefs])

    # Traverse student preference lists
    for i in range(1 + n, 1 + 2 * n):
        line = data[i].strip()
        prefs = list(map(int, line.split()))

        if len(prefs) != n or sorted(prefs) != list(range(1, n + 1)):
            sys.stderr.write(f"Invalid student preference list on line {i}.\n")
            sys.exit(1)

        student_prefs.append([h - 1 for h in prefs])
    return n, hospital_prefs, student_prefs


def gale_shapley(n, hospital_prefs, student_prefs):
    if n == 0:
        return []

    # Student ranking: rank[s][h] = preference order
    rank = [[0] * n for _ in range(n)]
    for s in range(n):
        for pos, h in enumerate(student_prefs[s]):
            rank[s][h] = pos

    next_proposal = [0] * n
    match_h = [-1] * n
    match_s = [-1] * n

    free = deque(range(n))

    while free:
        h = free.popleft()
        if next_proposal[h] >= n:
            continue  # Nobody left to propose to

        s = hospital_prefs[h][next_proposal[h]]
        next_proposal[h] += 1
        current = match_s[s]
        if current == -1: # Student is free
            match_h[h] = s
            match_s[s] = h
        else:  # Student compares current pairing vs new proposal
            if rank[s][h] < rank[s][current]:  # Student prefers the new hospital
                match_h[h] = s
                match_s[s] = h
                match_h[current] = -1

                if next_proposal[current] < n:
                    free.append(current)
            else:  # Student rejects h
                if next_proposal[h] < n:
                    free.append(h)
    return match_h


def main():
    n, hospital_prefs, student_prefs = read_input()
    matching = gale_shapley(n, hospital_prefs, student_prefs)

    for h in range(n):
        s = matching[h]
        sys.stdout.write(f"{h + 1} {s + 1}\n")


if __name__ == "__main__":
    main()
