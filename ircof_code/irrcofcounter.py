#Parses computational output files and statistically analyzes irreducible cofibrant families by cardinality

from collections import defaultdict
import re

filename = input("Enter filename: ").strip()

with open(filename, "r") as f:
    text = f.read()

pattern = r"irrcof\(S\)\s*=\s*\[(.*?)\]"

matches = re.findall(pattern, text)

groups = defaultdict(list)

for m in matches:

    if m.strip() == "":
        irr = []

    else:
        irr = [int(x.strip()) for x in m.split(",")]

    groups[len(irr)].append(irr)

print("\n" + "=" * 60)
print("IRRCOF GROUPED BY CARDINALITY")
print("=" * 60)

for k in sorted(groups):

    print(f"\nCardinality {k}")
    print("-" * 40)

    for irr in groups[k]:
        print(irr)

print("\n" + "=" * 60)
print("COUNTS")
print("=" * 60)

for k in sorted(groups):
    print(f"{k} irreducibles: {len(groups[k])}")