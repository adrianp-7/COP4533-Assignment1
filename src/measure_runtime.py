import time
import subprocess
import os

ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

matcher_times = []
verifier_times = []

for n in ns:
    infile = f"../data/large_n/n{n}.in"
    outfile = f"../data/large_n/n{n}.out"

    # Time matcher
    start = time.perf_counter()
    with open(infile) as f_in, open(outfile, "w") as f_out:
        subprocess.run(["python3", "matcher.py"], stdin=f_in, stdout=f_out)
    matcher_times.append(time.perf_counter() - start)

    # Time verifier
    start = time.perf_counter()
    with open(infile) as f_in, open(outfile) as f_out:
        subprocess.run(["python3", "verifier.py"], stdin=f_in)
    verifier_times.append(time.perf_counter() - start)

os.makedirs("../data/results", exist_ok=True)

with open("../data/results/matcher_times.txt", "w") as f:
    for n, t in zip(ns, matcher_times):
        f.write(f"{n} {t}\n")

with open("../data/results/verifier_times.txt", "w") as f:
    for n, t in zip(ns, verifier_times):
        f.write(f"{n} {t}\n")

