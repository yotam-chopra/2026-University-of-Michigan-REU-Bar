#This classifies which saturated transfer systems for cyclic groups actually arise from universes

from itertools import chain, combinations
from math import gcd

MODE = "nonrealizable"

def lcm(a, b):
    return a * b // gcd(a, b)

def divisors(n):
    out = []
    for d in range(1, n + 1):
        if n % d == 0:
            out.append(d)
    return sorted(out)

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(
        combinations(s, r) for r in range(len(s) + 1)
    )

def is_lcm_closed(S):

    S = set(S)

    if 1 not in S:
        return False

    for a in S:
        for b in S:
            if lcm(a, b) not in S:
                return False

    return True

def transfer_condition(U, a, b):

    lhs = set()

    for i in range(b):

        exists = False

        for j in U:
            if j % a == i % a:
                exists = True
                break

        if exists:
            lhs.add(i % b)

    rhs = {u % b for u in U}

    return lhs.issubset(rhs)

def transfer_system_from_universe(U, n):

    divs = divisors(n)

    S = set()

    for d in divs:

        if transfer_condition(U, 1, d):
            S.add(d)

    return tuple(sorted(S))

def realizable_systems(n):

    all_realizable = {}

    elements = list(range(n))

    rest = elements[1:]

    for subset in powerset(rest):

        U = {0} | set(subset)

        S = transfer_system_from_universe(U, n)

        if S not in all_realizable:
            all_realizable[S] = []

        all_realizable[S].append(sorted(U))

    return all_realizable

def main():

    n = 30

    divs = divisors(n)

    saturated = []

    for subset in powerset(divs):

        subset = tuple(sorted(subset))

        if is_lcm_closed(subset):
            saturated.append(subset)

    saturated = sorted(saturated, key=len)

    realizable = realizable_systems(n)

    print("=" * 70)
    print(f"REALIZABILITY RESULTS FOR C_{n}")
    print(f"MODE = {MODE}")
    print("=" * 70)
    print()

    realizable_count = 0
    nonrealizable_count = 0

    for S in saturated:

        is_realizable = S in realizable

        if MODE == "realizable" and not is_realizable:
            continue

        if MODE == "nonrealizable" and is_realizable:
            continue

        print(f"S = {S}")

        if is_realizable:

            realizable_count += 1

            print("  REALIZABLE")

            witness = realizable[S][0]

            print(f"  Witness universe:")
            print(f"  U = {witness}")

        else:

            nonrealizable_count += 1

            print("  NOT REALIZABLE")

        print()

    total_realizable = len(realizable)
    total_saturated = len(saturated)

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"Total saturated systems:     {total_saturated}")
    print(f"Total realizable systems:    {total_realizable}")
    print(f"Total nonrealizable systems: {total_saturated - total_realizable}")

if __name__ == "__main__":
    main()