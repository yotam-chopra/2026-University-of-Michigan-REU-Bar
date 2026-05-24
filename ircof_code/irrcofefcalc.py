from itertools import combinations, product
from math import gcd
from collections import defaultdict


def lcm(a, b):
    return a * b // gcd(a, b)


def divisors_from_prime_list(primes):

    exp_dict = {}

    for p in primes:
        exp_dict[p] = exp_dict.get(p, 0) + 1

    prime_powers = []

    for p, e in exp_dict.items():
        prime_powers.append([p**k for k in range(e + 1)])

    divisors = set()

    for tup in product(*prime_powers):

        x = 1

        for t in tup:
            x *= t

        divisors.add(x)

    return sorted(divisors)


def lcm_closure(gens, lcm_table):

    closure = set(gens)
    closure.add(1)

    frontier = list(gens)

    while frontier:

        a = frontier.pop()

        current = list(closure)

        for b in current:

            x = lcm_table[(a, b)]

            if x not in closure:

                closure.add(x)
                frontier.append(x)

    return frozenset(closure)


def irreducibles_of_closure(S, lcm_table):

    S = sorted(S)

    irr = []

    for a in S:

        if a == 1:
            continue

        reducible = False

        for i in range(len(S)):

            b = S[i]

            if b == a:
                continue

            for j in range(i, len(S)):

                c = S[j]

                if c == a:
                    continue

                if lcm_table[(b, c)] == a:
                    reducible = True
                    break

            if reducible:
                break

        if not reducible:
            irr.append(a)

    return tuple(sorted(irr))


def main():

    print("Enter prime factorization as repeated primes.")
    print("Example:")
    print("2 3 5 5 5")

    primes = list(map(int, input("\nPrimes: ").split()))

    divisors = divisors_from_prime_list(primes)

    print("\nNumber of divisors:", len(divisors))

    nontrivial = [d for d in divisors if d != 1]

    print("\nRequired irreducibles?")
    required_input = input("Must contain = ").strip()

    required = set()

    if required_input:
        required = set(map(int, required_input.split()))

    print("\nForbidden irreducibles?")
    forbidden_input = input("Must NOT contain = ").strip()

    forbidden = set()

    if forbidden_input:
        forbidden = set(map(int, forbidden_input.split()))

    lcm_table = {}

    for a in divisors:
        for b in divisors:
            lcm_table[(a, b)] = lcm(a, b)

    counts = defaultdict(int)

    seen = set()

    irr_seen = set()

    total = 0

    n = len(nontrivial)

    for r in range(len(required), n + 1):

        for extra in combinations(
            [x for x in nontrivial if x not in required and x not in forbidden],
            r - len(required)
        ):

            gens = set(required)
            gens.update(extra)

            closure = lcm_closure(gens, lcm_table)

            if closure in seen:
                continue

            seen.add(closure)

            irr = irreducibles_of_closure(closure, lcm_table)

            if not required.issubset(irr):
                continue

            if forbidden.intersection(irr):
                continue

            if irr in irr_seen:
                continue

            irr_seen.add(irr)

            counts[len(irr)] += 1

            total += 1

    print("\n")
    print("=" * 50)
    print("COUNTS BY NUMBER OF IRREDUCIBLES")
    print("=" * 50)

    for k in sorted(counts):
        print(f"{k}: {counts[k]}")

    print("\nTotal distinct irreducible families:")
    print(total)


if __name__ == "__main__":
    main()