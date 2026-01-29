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

# Create figure with subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
ax1, ax2, ax3 = axes

# Matcher plot
ax1.plot(ns_m, t_m, marker="o", linewidth=2, markersize=8, color='blue')
ax1.set_xlabel("n", fontsize=11)
ax1.set_ylabel("Runtime (seconds)", fontsize=11)
ax1.set_title("Matcher Runtime", fontsize=13, fontweight='bold')
ax1.set_xscale("log", base=2)
ax1.set_yscale("log")
ax1.grid(True, alpha=0.3)

# Verifier plot
ax2.plot(ns_v, t_v, marker="s", linewidth=2, markersize=8, color='red')
ax2.set_xlabel("n", fontsize=11)
ax2.set_ylabel("Runtime (seconds)", fontsize=11)
ax2.set_title("Verifier Runtime", fontsize=13, fontweight='bold')
ax2.set_xscale("log", base=2)
ax2.set_yscale("log")
ax2.grid(True, alpha=0.3)

# Combined plot
ax3.plot(ns_m, t_m, marker="o", linewidth=2, markersize=8, label="Matcher", color='blue')
ax3.plot(ns_v, t_v, marker="s", linewidth=2, markersize=8, label="Verifier", color='red')
ax3.set_xlabel("n", fontsize=11)
ax3.set_ylabel("Runtime (seconds)", fontsize=11)
ax3.set_title("Matcher vs Verifier Runtime", fontsize=13, fontweight='bold')
ax3.set_xscale("log", base=2)
ax3.set_yscale("log")
ax3.grid(True, alpha=0.3)
ax3.legend()

plt.tight_layout()

# Show interactive window
plt.ion()  # Turn on interactive mode
plt.show()

# Save static versions
plt.savefig("../graphs/runtime_matcher.png", dpi=300, bbox_inches='tight')
plt.savefig("../graphs/runtime_verifier.png", dpi=300, bbox_inches='tight')
plt.savefig("../graphs/combined_runtime.png", dpi=300, bbox_inches='tight')

print("Graphs displayed! Close the window when done.")
input("Press Enter to exit...")