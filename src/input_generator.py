import random
import os


# Populate data for each instance of n up to 512

def generate_instance(n, path):
    with open(path, "w") as f:
        f.write(str(n) + "\n")
        for _ in range(n):
            prefs = list(range(1, n+1))
            random.shuffle(prefs)
            f.write(" ".join(map(str, prefs)) + "\n")
        for _ in range(n):
            prefs = list(range(1, n+1))
            random.shuffle(prefs)
            f.write(" ".join(map(str, prefs)) + "\n")


if __name__ == "__main__":
    ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    os.makedirs("../data/large_n", exist_ok=True)
    for n in ns:
        generate_instance(n, f"../data/large_n/n{n}.in")

