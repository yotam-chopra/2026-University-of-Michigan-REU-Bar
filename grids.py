import math
import os
from itertools import product
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def factorization(n):

    fac = {}

    d = 2

    while d * d <= n:

        while n % d == 0:

            fac[d] = fac.get(d, 0) + 1

            n //= d

        d += 1

    if n > 1:
        fac[n] = fac.get(n, 0) + 1

    return fac


def crt_coordinates(n, prime_powers):

    coords = {}

    for x in range(n):

        coords[x] = tuple(
            x % pp
            for pp in prime_powers
        )

    return coords


def build_multibox_grid(n):

    fac = factorization(n)

    prime_powers = [
        p ** e
        for p, e in fac.items()
    ]

    coords = crt_coordinates(n, prime_powers)

    if len(prime_powers) == 1:

        layers = 1
        rows = 1
        cols = prime_powers[0]

    elif len(prime_powers) == 2:

        layers = 1
        rows = prime_powers[0]
        cols = prime_powers[1]

    else:

        layers = prime_powers[2]

        rows = prime_powers[0]
        cols = prime_powers[1]

    grids = []

    for _ in range(layers):

        grids.append([
            [None for _ in range(cols)]
            for _ in range(rows)
        ])

    for x in range(n):

        c = coords[x]

        if len(prime_powers) == 1:

            layer = 0
            row = 0
            col = c[0]

        elif len(prime_powers) == 2:

            layer = 0
            row = c[0]
            col = c[1]

        else:

            row = c[0]
            col = c[1]
            layer = c[2]

        grids[layer][row][col] = x

    return grids


def deletion_condition(x, deletions):

    for modulus, residue in deletions:

        if x % modulus == residue % modulus:
            return True

    return False


def draw_layer(
    ax,
    grid,
    deletions,
    title=""
):

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):

            x = grid[r][c]

            color = "lightgray"

            if deletion_condition(x, deletions):
                color = "lightcoral"

            rect = Rectangle(
                (c, rows - r - 1),
                1,
                1,
                facecolor=color,
                edgecolor="black",
                linewidth=1
            )

            ax.add_patch(rect)

            ax.text(
                c + 0.5,
                rows - r - 0.5,
                str(x),
                ha="center",
                va="center",
                fontsize=8
            )

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)

    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))

    ax.set_aspect("equal")

    ax.set_title(title)


def generate_diagrams(
    n,
    irreducibles
):

    folder_name = (
        f"CRT_n_{n}_irr_" +
        "_".join(map(str, irreducibles))
    )

    os.makedirs(folder_name, exist_ok=True)

    grids = build_multibox_grid(n)

    max_per_row = 5

    num_layers = len(grids)

    num_rows = math.ceil(num_layers / max_per_row)

    num_cols = min(max_per_row, num_layers)

    # --------------------------------------------------------
    # Individual irreducible diagrams
    # --------------------------------------------------------

    for irr in irreducibles:

        fig, axs = plt.subplots(
            num_rows,
            num_cols,
            figsize=(4 * num_cols, 4 * num_rows)
        )

        if num_rows == 1 and num_cols == 1:
            axs = [[axs]]

        elif num_rows == 1:
            axs = [axs]

        elif num_cols == 1:
            axs = [[a] for a in axs]

        axs_flat = [
            ax
            for row in axs
            for ax in row
        ]

        for i, grid in enumerate(grids):

            draw_layer(
                axs_flat[i],
                grid,
                deletions=[(irr, 0)],
                title=f"Layer {i}"
            )

        for j in range(len(grids), len(axs_flat)):
            axs_flat[j].axis("off")

        plt.suptitle(
            f"Delete class mod {irr}",
            fontsize=18
        )

        plt.tight_layout()

        filename = os.path.join(
            folder_name,
            f"mod_{irr}.png"
        )

        plt.savefig(
            filename,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print(f"Saved {filename}")

    # --------------------------------------------------------
    # Full transfer system
    # --------------------------------------------------------

    fig, axs = plt.subplots(
        num_rows,
        num_cols,
        figsize=(4 * num_cols, 4 * num_rows)
    )

    if num_rows == 1 and num_cols == 1:
        axs = [[axs]]

    elif num_rows == 1:
        axs = [axs]

    elif num_cols == 1:
        axs = [[a] for a in axs]

    axs_flat = [
        ax
        for row in axs
        for ax in row
    ]

    deletions = [
        (irr, 0)
        for irr in irreducibles
    ]

    for i, grid in enumerate(grids):

        draw_layer(
            axs_flat[i],
            grid,
            deletions=deletions,
            title=f"Layer {i}"
        )

    for j in range(len(grids), len(axs_flat)):
        axs_flat[j].axis("off")

    plt.suptitle(
        "Full Transfer System",
        fontsize=18
    )

    plt.tight_layout()

    filename = os.path.join(
        folder_name,
        "full_transfer_system.png"
    )

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved {filename}")


if __name__ == "__main__":

    n = int(input("Enter n: "))

    print()
    print("Enter irreducible cofibrants.")
    print("Example: 2 11 33")
    print()

    irreducibles = list(
        map(
            int,
            input("Irreducibles: ").split()
        )
    )

    generate_diagrams(
        n,
        irreducibles
    )