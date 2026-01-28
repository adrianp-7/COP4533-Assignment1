import sys


def read_input_and_matching():
    """Read the input file with preferences and matching from stdin"""
    # Read all lines from stdin
    all_lines = []
    for line in sys.stdin:
        all_lines.append(line.rstrip('\n'))
    
    if not all_lines:
        return 0, [], [], []

    try:
        n = int(all_lines[0].strip())
    except ValueError:
        sys.stderr.write("Invalid input: first line must be an integer n.\n")
        sys.exit(1)

    if n < 0:
        sys.stderr.write("Invalid input: n must be a positive integer.\n")
        sys.exit(1)

    if n == 0:
        # For n=0, there should be no more lines (or just empty lines)
        matching_lines = [line for line in all_lines[1:] if line.strip()]
        return 0, [], [], matching_lines

    # Check we have enough lines for preferences
    if len(all_lines) < 1 + 2 * n:
        sys.stderr.write("Invalid input: not enough preference lines.\n")
        sys.exit(1)

    hospital_prefs = []
    student_prefs = []

    # Read hospital preference lists
    for i in range(1, 1 + n):
        line = all_lines[i].strip()
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

    # Read student preference lists
    for i in range(1 + n, 1 + 2 * n):
        line = all_lines[i].strip()
        try:
            prefs = list(map(int, line.split()))
        except ValueError:
            sys.stderr.write(f"Invalid input: non-integer in student preference line {i}.\n")
            sys.exit(1)

        if len(prefs) != n or sorted(prefs) != list(range(1, n + 1)):
            sys.stderr.write(f"Invalid student preference list on line {i}.\n")
            sys.exit(1)

        student_prefs.append([h - 1 for h in prefs])

    # Read matching lines (everything after preferences)
    matching_lines = all_lines[1 + 2 * n:]

    return n, hospital_prefs, student_prefs, matching_lines


def parse_matching(matching_lines, n):
    """Parse matching lines and return dictionaries mapping hospital->student and student->hospital
    Returns (match_h, match_s, error_message) where error_message is None if successful"""
    match_h = {}  # hospital -> student (0-indexed)
    match_s = {}  # student -> hospital (0-indexed)

    for line in matching_lines:
        parts = line.strip().split()
        if len(parts) != 2:
            return None, None, f"matching line '{line}' has invalid format (expected two integers)"

        try:
            h = int(parts[0]) - 1  # Convert to 0-indexed
            s = int(parts[1]) - 1  # Convert to 0-indexed
        except ValueError:
            return None, None, f"matching line '{line}' contains non-integer values"

        if h < 0 or h >= n or s < 0 or s >= n:
            return None, None, f"matching line '{line}' contains ID out of range [1, {n}]"

        if h in match_h:
            return None, None, f"hospital {h + 1} appears multiple times"

        if s in match_s:
            return None, None, f"student {s + 1} appears multiple times"

        match_h[h] = s
        match_s[s] = h

    return match_h, match_s, None


def check_validity(match_h, match_s, n):
    """Check that each hospital and each student is matched to exactly one partner
    Returns (is_valid, error_message)"""
    # Check all hospitals are matched
    if len(match_h) != n:
        return False, f"expected {n} hospitals, found {len(match_h)}"

    # Check all students are matched
    if len(match_s) != n:
        return False, f"expected {n} students, found {len(match_s)}"

    # Check that matches are consistent (hospital h matched to student s implies student s matched to hospital h)
    for h, s in match_h.items():
        if s not in match_s or match_s[s] != h:
            return False, f"inconsistent match between hospital {h + 1} and student {s + 1}"

    return True, None


def check_stability(match_h, match_s, hospital_prefs, student_prefs, n):
    """Check that there are no blocking pairs
    Returns (is_stable, blocking_pair_info)"""
    # Build rank arrays for efficient preference checking
    # rank_h[h][s] = position of student s in hospital h's preference list
    rank_h = [[0] * n for _ in range(n)]
    for h in range(n):
        for pos, s in enumerate(hospital_prefs[h]):
            rank_h[h][s] = pos

    # rank_s[s][h] = position of hospital h in student s's preference list
    rank_s = [[0] * n for _ in range(n)]
    for s in range(n):
        for pos, h in enumerate(student_prefs[s]):
            rank_s[s][h] = pos

    # Check for blocking pairs
    for h in range(n):
        current_student = match_h[h]
        for s in range(n):
            # Skip if this is the current match
            if s == current_student:
                continue

            # Check if hospital h prefers student s over current match
            h_prefers_s = rank_h[h][s] < rank_h[h][current_student]

            if h_prefers_s:
                # Check if student s prefers hospital h over their current match
                current_hospital = match_s[s]
                s_prefers_h = rank_s[s][h] < rank_s[s][current_hospital]

                if s_prefers_h:
                    # Found a blocking pair!
                    return False, f"({h + 1}, {s + 1})"

    return True, None


def main():
    # Read input preferences and matching
    n, hospital_prefs, student_prefs, matching_lines = read_input_and_matching()

    if n == 0:
        # Empty matching for n=0
        if matching_lines:
            print("INVALID: expected empty output for n=0")
            sys.exit(1)
        print("VALID STABLE")
        return

    # Parse matching
    match_h, match_s, parse_error = parse_matching(matching_lines, n)
    if parse_error is not None:
        print(f"INVALID: {parse_error}")
        sys.exit(1)

    # Check validity
    is_valid, validity_error = check_validity(match_h, match_s, n)
    
    # Check stability (only if valid)
    is_stable, blocking_pair = None, None
    if is_valid:
        is_stable, blocking_pair = check_stability(match_h, match_s, hospital_prefs, student_prefs, n)

    # Output results according to format
    if is_valid and is_stable:
        print("VALID STABLE")
    else:
        output_parts = []
        if not is_valid:
            output_parts.append(f"INVALID: {validity_error}")
        if is_stable is not None and not is_stable:
            output_parts.append(f"UNSTABLE: blocking pair {blocking_pair}")
        
        # Output all errors (or just one if both exist - we'll output both)
        print(" ".join(output_parts))
        sys.exit(1)


if __name__ == "__main__":
    main()
