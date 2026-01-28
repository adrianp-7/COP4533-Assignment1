import matplotlib.pyplot as plt


def load_times(path):
    ns, ts = [], []
    with open(path) as f:
        for line in f:
            n, t = line.split()
            ns.append(int(n))
            ts.append(float(t))
    return ns, ts


ns_m, t_m = load_times("../data/results/matcher_times.txt")
ns_v, t_v = load_times("../data/results/verifier_times.txt")

plt.plot(ns_m, t_m, marker="o")
plt.xlabel("n")
plt.ylabel("Runtime (seconds)")
plt.title("Matcher Runtime")
plt.xscale("log", base=2)
plt.savefig("../graphs/runtime_matcher.png")
plt.clf()

plt.plot(ns_v, t_v, marker="o", color="red")
plt.xlabel("n")
plt.ylabel("Runtime (seconds)")
plt.title("Verifier Runtime")
plt.xscale("log", base=2)
plt.savefig("../graphs/runtime_verifier.png")
plt.clf()

plt.plot(ns_m, t_m, marker="o", label="Matcher")
plt.plot(ns_v, t_v, marker="o", label="Verifier")
plt.xlabel("n")
plt.ylabel("Runtime (seconds)")
plt.title("Matcher vs Verifier Runtime")
plt.xscale("log", base=2)
plt.legend()
plt.savefig("../graphs/combined_runtime.png")

