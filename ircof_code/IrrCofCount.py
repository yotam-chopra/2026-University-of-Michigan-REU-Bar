#Enumerates and classifies LCM-closed divisor systems of squarefree integers by their irreducible generators

from itertools import combinations, chain
from math import gcd

def lcm(a, b):
    return a * b // gcd(a, b)

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def divisors_from_primes(primes):

    divs = {1}

    for p in primes:

        new_divs = set()

        for d in divs:
            new_divs.add(d)
            new_divs.add(d * p)

        divs = new_divs

    return sorted(divs)

def is_lcm_closed(S):

    S = set(S)

    if 1 not in S:
        return False

    for a in S:
        for b in S:

            if lcm(a, b) not in S:
                return False

    return True

def irreducible_elements(S):

    S = set(S)

    irr = []

    for a in S:

        if a == 1:
            continue

        reducible = False

        for b in S:
            for c in S:

                if lcm(b, c) == a:

                    if b != a and c != a:
                        reducible = True

        if not reducible:
            irr.append(a)

    return sorted(irr)

def main():

    print("Enter distinct primes separated by spaces.")
    print("Example: 2 3 5")

    primes = list(map(int, input("Primes: ").split()))

    n = 1

    for p in primes:
        n *= p

    divisors = divisors_from_primes(primes)

    print("\n----------------------------------------")
    print(f"n = {n}")
    print(f"Div(n) = {divisors}")
    print("----------------------------------------\n")

    print("Required irreducible cofibrants?")
    print("Example: 3 6")
    print("Leave blank for none.")

    required_input = input("Must contain = ").strip()

    required = set()

    if required_input != "":
        required = set(map(int, required_input.split()))

    print("\nForbidden irreducible cofibrants?")
    print("Example: 2")
    print("Leave blank for none.")

    forbidden_input = input("Must NOT contain = ").strip()

    forbidden = set()

    if forbidden_input != "":
        forbidden = set(map(int, forbidden_input.split()))

    valid_sets = []

    for subset in powerset(divisors):

        subset = set(subset)

        if is_lcm_closed(subset):

            irr = irreducible_elements(subset)

            if not required.issubset(set(irr)):
                continue

            if set(irr).intersection(forbidden):
                continue

            valid_sets.append(sorted(subset))

    valid_sets.sort(key=len)

    print(f"\nTotal matching LCM-closed subsets: {len(valid_sets)}\n")

    size_counts = {}
    irr_counts = {}

    for S in valid_sets:

        s = len(S)

        size_counts[s] = size_counts.get(s, 0) + 1

        irr_num = len(irreducible_elements(S))

        irr_counts[irr_num] = irr_counts.get(irr_num, 0) + 1

    current_size = None

    for S in valid_sets:

        if len(S) != current_size:

            current_size = len(S)

            if current_size == 2:
                label = "Pairs"

            elif current_size == 3:
                label = "Triplets"

            elif current_size == 4:
                label = "Quadruples"

            else:
                label = f"Size {current_size}"

            print("=" * 50)
            print(label)
            print("=" * 50)

        irr = irreducible_elements(S)

        print(f"S = {S}")
        print(f"irrcof(S) = {irr}")
        print()

    print("\n")
    print("=" * 60)
    print("SUMMARY COUNTS")
    print("=" * 60)

    print("\nCounts by size:")

    for s in sorted(size_counts):
        print(f"Size {s}: {size_counts[s]}")

    print("\nCounts by number of irreducible cofibrants:")

    for r in sorted(irr_counts):
        print(f"{r} irreducibles: {irr_counts[r]}")

if __name__ == "__main__":
    main()