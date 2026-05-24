#This computes transfer systems on cyclic groups induced by a chosen universe of characters


def divisors(n):

    divs = []

    for i in range(1, int(n**0.5) + 1):

        if n % i == 0:

            divs.append(i)

            if i != n // i:
                divs.append(n // i)

    return sorted(divs)


def prime_divisors(n):

    primes = []

    d = 2

    while d * d <= n:

        if n % d == 0:

            primes.append(d)

            while n % d == 0:
                n //= d

        d += 1

    if n > 1:
        primes.append(n)

    return primes


def possible_edges(n):

    divs = divisors(n)

    edges = []

    for d in divs:

        for p in prime_divisors(n // d):

            if d * p in divs:

                edges.append((d, d * p))

    return edges


def transfer_graph_from_universe(n, U):

    divs = divisors(n)

    edges = set()

    for d in divs:

        for p in prime_divisors(n // d):

            pd = p * d

            if pd not in divs:
                continue

            valid = True

            for k in U:

                if k % d == 0:

                    if k % pd != 0:

                        valid = False
                        break

            if valid:
                edges.add((d, pd))

    return edges


def print_transfer_graph(G):

    if not G:
        print("{}")
        return

    for e in sorted(G):

        print(f"C_{e[0]} -> C_{e[1]}")


while True:

    print("\n==============================")
    print(" Universe -> Transfer System ")
    print("==============================")

    user_input = input("\nEnter n for C_n (or q to quit): ")

    if user_input.lower() == "q":
        break

    n = int(user_input)

    print(f"\nCharacters are 0 through {n-1}")

    print("\nEnter universe elements separated by spaces.")
    print("Example: 0 4 8")

    U_input = input("\nUniverse U = ")

    U = set(map(int, U_input.strip().split()))

    if 0 not in U:
        print("\nWARNING: adding trivial character 0 automatically.")
        U.add(0)

    print("\nUniverse:")
    print(sorted(U))

    G = transfer_graph_from_universe(n, U)

    print("\nTransfer System:")

    print_transfer_graph(G)

    print("\nAll possible prime-step edges:")

    print(sorted(possible_edges(n)))