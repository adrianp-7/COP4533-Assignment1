import sys


def read_input_and_matching():
    """Read preferences and matching from stdin.

    Returns (n, hospital_prefs, student_prefs, matching_lines).
    """
    lines = sys.stdin.read().strip().splitlines() if sys.stdin else []

    if not lines:
        return 0, [], [], []

    try:
        n = int(lines[0].strip())
    except ValueError:
        sys.stderr.write("Invalid input: first line must be an integer n.\n")
        sys.exit(1)

    if n < 0:
        sys.stderr.write("Invalid input: n must be a positive integer.\n")
        sys.exit(1)

    if n == 0:
        matching_lines = [line for line in lines[1:] if line.strip()]
        return 0, [], [], matching_lines

    if len(lines) < 1 + 2 * n:
        sys.stderr.write("Invalid input: not enough preference lines.\n")
        sys.exit(1)

    hospital_prefs = []
    student_prefs = []

    # Read hospital preference lists (lines 1 to n)
    for i in range(1, 1 + n):
        prefs = parse_preference_line(lines[i], i, n, "hospital")
        hospital_prefs.append([s - 1 for s in prefs])

    # Read student preference lists (lines n+1 to 2n)
    for i in range(1 + n, 1 + 2 * n):
        prefs = parse_preference_line(lines[i], i, n, "student")
        student_prefs.append([h - 1 for h in prefs])

    matching_lines = lines[1 + 2 * n:]
    return n, hospital_prefs, student_prefs, matching_lines


def parse_preference_line(line, line_num, n, entity_type):
    """Parse a single preference line and validate it.

    Returns the list of preferences (1-indexed) or exits on error.
    """
    line = line.strip()
    if not line:
        sys.stderr.write(f"Invalid input: empty {entity_type} preference line {line_num}.\n")
        sys.exit(1)

    try:
        prefs = list(map(int, line.split()))
    except ValueError:
        sys.stderr.write(f"Invalid input: non-integer in {entity_type} preference line {line_num}.\n")
        sys.exit(1)

    expected = list(range(1, n + 1))
    if len(prefs) != n or sorted(prefs) != expected:
        sys.stderr.write(f"Invalid {entity_type} preference list on line {line_num}.\n")
        sys.exit(1)

    return prefs


def parse_matching(matching_lines, n):
    """Parse matching lines into hospital->student and student->hospital mappings.

    Returns (match_h, match_s, error_message) where error_message is None if successful.
    All indices are 0-based.
    """
    match_h = {}
    match_s = {}

    for line in matching_lines:
        parts = line.strip().split()
        if len(parts) != 2:
            return None, None, f"matching line '{line}' has invalid format (expected two integers)"

        try:
            h = int(parts[0]) - 1
            s = int(parts[1]) - 1
        except ValueError:
            return None, None, f"matching line '{line}' contains non-integer values"

        if not (0 <= h < n and 0 <= s < n):
            return None, None, f"matching line '{line}' contains ID out of range [1, {n}]"

        if h in match_h:
            return None, None, f"hospital {h + 1} appears multiple times"

        if s in match_s:
            return None, None, f"student {s + 1} appears multiple times"

        match_h[h] = s
        match_s[s] = h

    return match_h, match_s, None


def check_validity(match_h, match_s, n):
    """Check that each hospital and student is matched exactly once.

    Returns (is_valid, error_message).
    """
    if len(match_h) != n:
        return False, f"expected {n} hospitals, found {len(match_h)}"

    if len(match_s) != n:
        return False, f"expected {n} students, found {len(match_s)}"

    for h, s in match_h.items():
        if match_s.get(s) != h:
            return False, f"inconsistent match between hospital {h + 1} and student {s + 1}"

    return True, None


def build_rank_matrix(prefs, n):
    """Build a rank matrix from preference lists.

    rank[i][j] = position of j in entity i's preference list.
    """
    rank = [[0] * n for _ in range(n)]
    for i in range(n):
        for pos, j in enumerate(prefs[i]):
            rank[i][j] = pos
    return rank


def check_stability(match_h, match_s, hospital_prefs, student_prefs, n):
    """Check that there are no blocking pairs.

    A blocking pair (h, s) exists when:
    - h prefers s over their current match, AND
    - s prefers h over their current match

    Returns (is_stable, blocking_pair_info).
    """
    rank_h = build_rank_matrix(hospital_prefs, n)
    rank_s = build_rank_matrix(student_prefs, n)

    for h in range(n):
        current_student = match_h[h]
        h_rank_of_current = rank_h[h][current_student]

        for s in range(n):
            if s == current_student:
                continue

            h_prefers_s = rank_h[h][s] < h_rank_of_current
            if not h_prefers_s:
                continue

            current_hospital = match_s[s]
            s_prefers_h = rank_s[s][h] < rank_s[s][current_hospital]
            if s_prefers_h:
                return False, f"({h + 1}, {s + 1})"

    return True, None


def main():
    n, hospital_prefs, student_prefs, matching_lines = read_input_and_matching()

    # Handle empty case
    if n == 0:
        if matching_lines:
            print("INVALID: expected empty output for n=0")
            sys.exit(1)
        print("VALID STABLE")
        return

    # Parse the matching
    match_h, match_s, parse_error = parse_matching(matching_lines, n)
    if parse_error:
        print(f"INVALID: {parse_error}")
        sys.exit(1)

    # Validate the matching
    is_valid, validity_error = check_validity(match_h, match_s, n)
    if not is_valid:
        print(f"INVALID: {validity_error}")
        sys.exit(1)

    # Check for stability
    is_stable, blocking_pair = check_stability(match_h, match_s, hospital_prefs, student_prefs, n)
    if not is_stable:
        print(f"UNSTABLE: blocking pair {blocking_pair}")
        sys.exit(1)

    print("VALID STABLE")


if __name__ == "__main__":
    main()
