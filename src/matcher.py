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



def main():
    n, hospital_prefs, student_prefs = read_input()


if __name__ == "__main__":
    main()
