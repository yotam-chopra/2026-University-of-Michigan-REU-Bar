import math
import itertools
import numpy as np
import matplotlib.pyplot as plt
from sympy import factorint


n = int(input("Enter n: "))
mods = list(map(int, input("Enter subset mods separated by spaces: ").split()))

f = factorint(n)

prime_list = []

for p, e in sorted(f.items()):
    for _ in range(e):
        prime_list.append(p)

if len(prime_list) < 2:
    raise ValueError("Need at least two prime factors")

rows = prime_list[0]
cols = prime_list[1]

layer_dims = prime_list[2:]

layers = 1
for d in layer_dims:
    layers *= d

all_layers = []

count = 0

for L in range(layers):
    grid = np.zeros((rows, cols), dtype=int)

    for r in range(rows):
        for c in range(cols):
            grid[r, c] = count
            count += 1

    all_layers.append(grid)

coverage = np.zeros((layers, rows, cols), dtype=int)

colors = {
    0: "lightgray",
    1: "#ff6666",
    2: "#66cc66",
    3: "#6699ff",
    4: "#ffcc33",
    5: "#bb66cc",
    6: "#66dddd",
    7: "#ff99aa",
    8: "#ffaa44"
}


def layer_coords(L):
    coords = []

    x = L

    for d in reversed(layer_dims):
        coords.append(x % d)
        x //= d

    coords.reverse()

    return coords


def coords_to_layer(coords):
    x = 0

    for i in range(len(coords)):
        x *= layer_dims[i]
        x += coords[i]

    return x


def canonical_pattern(m):
    mf = factorint(m)

    active = []

    for p, e in mf.items():
        active += [p] * e

    active = sorted(active)

    use_row = False
    use_col = False

    use_layers = [False] * len(layer_dims)

    ptr = 0

    if ptr < len(active) and active[ptr] == rows:
        use_row = True
        ptr += 1

    if ptr < len(active) and active[ptr] == cols:
        use_col = True
        ptr += 1

    for i, d in enumerate(layer_dims):
        if ptr < len(active) and active[ptr] == d:
            use_layers[i] = True
            ptr += 1

    return use_row, use_col, use_layers


def generate_all_translations(m):
    use_row, use_col, use_layers = canonical_pattern(m)

    row_choices = [0]
    col_choices = [cols - 1]

    layer_choices = []

    if use_row:
        row_choices = list(range(rows))

    if use_col:
        col_choices = list(range(cols))

    for i, d in enumerate(layer_dims):
        if use_layers[i]:
            layer_choices.append(list(range(d)))
        else:
            layer_choices.append([None])

    all_regions = []

    for rpick in row_choices:
        for cpick in col_choices:
            for lpicks in itertools.product(*layer_choices):

                region = set()

                for L in range(layers):
                    lc = layer_coords(L)

                    ok_layer = True

                    for i in range(len(layer_dims)):
                        if use_layers[i]:
                            if lc[i] != lpicks[i]:
                                ok_layer = False
                                break

                    if not ok_layer:
                        continue

                    for r in range(rows):
                        for c in range(cols):

                            ok = True

                            if use_row and r != rpick:
                                ok = False

                            if use_col and c != cpick:
                                ok = False

                            if ok:
                                region.add((L, r, c))

                all_regions.append(region)

    return all_regions


mods_sorted = sorted(mods)

placed_regions = {}

for idx, m in enumerate(mods_sorted):
    patterns = generate_all_translations(m)

    best_pattern = None
    best_gain = -1

    for pat in patterns:
        gain = 0

        for (L, r, c) in pat:
            if coverage[L, r, c] == 0:
                gain += 1

        if gain > best_gain:
            best_gain = gain
            best_pattern = pat

    placed_regions[m] = best_pattern

    for (L, r, c) in best_pattern:
        coverage[L, r, c] = idx + 1


grid_cols = math.ceil(math.sqrt(layers))
grid_rows = math.ceil(layers / grid_cols)

fig, axes = plt.subplots(
    grid_rows,
    grid_cols,
    figsize=(4 * grid_cols, 4 * grid_rows)
)

axes = np.array(axes).reshape(-1)

fig.suptitle(
    f"Greedy CRT packing for n={n}, mods={mods}",
    fontsize=18
)

for idx, ax in enumerate(axes):
    if idx >= layers:
        ax.axis("off")
        continue

    grid = all_layers[idx]

    for r in range(rows):
        for c in range(cols):
            val = coverage[idx, r, c]

            rect = plt.Rectangle(
                (c, rows - 1 - r),
                1,
                1,
                facecolor=colors[val],
                edgecolor="black"
            )

            ax.add_patch(rect)

            ax.text(
                c + 0.5,
                rows - 1 - r + 0.5,
                str(grid[r, c]),
                ha="center",
                va="center",
                fontsize=6
            )

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)

    ax.set_xticks(range(cols + 1))
    ax.set_yticks(range(rows + 1))

    ax.set_title(f"Layer {idx}", fontsize=9)

    ax.set_aspect("equal")

plt.tight_layout()
plt.show()