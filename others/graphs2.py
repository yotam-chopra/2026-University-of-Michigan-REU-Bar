#this enumerates all transfer systems on cyclic subgroup lattices by brute-force checking of transfer axioms

from itertools import combinations, chain
import string
import networkx as nx
import matplotlib.pyplot as plt

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def divides(a, b):
    return b % a == 0

def subgroup_intersection(a, b):
    import math
    return math.gcd(a, b)

def divisor_from_expvec(expvec, primes):
    out = 1
    for p, e in zip(primes, expvec):
        out *= p**e
    return out

num_primes = int(input("Number of distinct primes: "))

prime_names = []
prime_powers = []

for i in range(num_primes):
    p = input(f"Prime label {i+1} (example p,q,r): ")
    e = int(input(f"Exponent of {p}: "))
    prime_names.append(p)
    prime_powers.append(e)

exp_vectors = [[]]

for emax in prime_powers:
    new = []
    for v in exp_vectors:
        for e in range(emax + 1):
            new.append(v + [e])
    exp_vectors = new

def symbolic_label(vec):
    pieces = []
    for p, e in zip(prime_names, vec):
        if e == 0:
            continue
        elif e == 1:
            pieces.append(p)
        else:
            pieces.append(f"{p}^{e}")
    return "1" if not pieces else "".join(pieces)

labels = [symbolic_label(v) for v in exp_vectors]

actual_primes = [2,3,5,7,11,13,17,19][:num_primes]

divisor_data = []

for vec, label in zip(exp_vectors, labels):
    divisor_data.append({
        "vec": vec,
        "label": label,
        "num": divisor_from_expvec(vec, actual_primes)
    })

divisor_data.sort(key=lambda x: x["num"])

pairs = []

for A in divisor_data:
    for B in divisor_data:
        if A["num"] < B["num"] and divides(A["num"], B["num"]):
            pairs.append((A, B))

letters = list(string.ascii_lowercase)

edge_labels = {}

for i, (A, B) in enumerate(pairs):
    if i < len(letters):
        edge_labels[letters[i]] = (A["label"], B["label"])
    else:
        edge_labels[f"x{i}"] = (A["label"], B["label"])

print("\n===================================================")
print("EDGE LABELS")
print("===================================================\n")

for k, v in edge_labels.items():
    print(f"{k}: {v[0]} -> {v[1]}")

G = nx.DiGraph()

for d in divisor_data:
    G.add_node(d["label"])

for k, (u, v) in edge_labels.items():
    G.add_edge(u, v, label=k)

plt.figure(figsize=(10, 7))

pos = nx.spring_layout(G, seed=2)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=2500,
    font_size=11,
    arrows=True
)

edge_draw_labels = {
    (u, v): k
    for k, (u, v) in edge_labels.items()
}

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_draw_labels,
    font_color='red'
)

plt.title("Comparable subgroup pairs")
plt.show()

pair_lookup = {}

for k, (u, v) in edge_labels.items():
    pair_lookup[k] = (u, v)

def check_transitivity(relset):
    relpairs = [pair_lookup[x] for x in relset]

    for (a, b) in relpairs:
        for (c, d) in relpairs:
            if b == c:
                if (a, d) in relpairs:
                    continue

                found = False

                for x in relset:
                    if pair_lookup[x] == (a, d):
                        found = True
                        break

                if not found:
                    return False

    return True

def check_restriction(relset):

    label_to_num = {
        d["label"]: d["num"]
        for d in divisor_data
    }

    relpairs = [pair_lookup[x] for x in relset]

    for (K, H) in relpairs:

        Knum = label_to_num[K]
        Hnum = label_to_num[H]

        for L in divisor_data:

            Llab = L["label"]
            Lnum = L["num"]

            if divides(Lnum, Hnum):

                import math

                inter_num = math.gcd(Knum, Lnum)

                inter_label = None

                for d in divisor_data:
                    if d["num"] == inter_num:
                        inter_label = d["label"]
                        break

                needed = (inter_label, Llab)

                exists = False

                for x in relset:
                    if pair_lookup[x] == needed:
                        exists = True
                        break

                if not exists and needed[0] != needed[1]:
                    return False

    return True

all_labels = list(edge_labels.keys())

valid = []

for subset in powerset(all_labels):

    subset = set(subset)

    if check_transitivity(subset) and check_restriction(subset):
        valid.append(subset)

print("\n===================================================")
print("TRANSFER SYSTEMS")
print("===================================================\n")

for i, ts in enumerate(valid, start=1):

    if len(ts) == 0:
        name = "0"
    else:
        name = "".join(sorted(ts))

    print(f"{i}: {name}")

print("\n===================================================")
print("TOTAL")
print("===================================================\n")

print(len(valid))