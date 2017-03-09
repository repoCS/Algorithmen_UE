#!/usr/bin/env python3

import sys

def parse_file(path):
    parse_g_down = True
    down_weights = []
    right_weights = []

    # Handle individual lines
    with open(path, "r") as in_file:
        for line in in_file:
            if line.startswith("G_down:"):
                tmp = line.rstrip("\n").split(" ")
                n, m = int(tmp[1]) + 1, int(tmp[2])
            elif line.startswith("G_right:"):
                parse_g_down = False
            elif line == "---\n":
                continue
            else:
                tmp = line.strip(" ").rstrip("\n").split("   ")
                if parse_g_down == True:
                    down_weights.append(tmp)
                else:
                    right_weights.append(tmp)

    return [down_weights, right_weights, n, m]


def manhattan_tourist(w_down, w_right, n, m):
    # Initialize graph
    s = [[], ] * n
    for i in range(0, n):
        s[i] = [0, ] * m

    # Insert first row
    for i in range(1, n):
        del s[i][0]
        s[i].insert(0, round(s[i-1][0] + float(w_down[i-1][0]), 2))

    # Insert first column
    for i in range(1, m):
        del s[0][i]
        s[0].insert(i, round(s[0][i-1] + float(w_right[i-1][0]), 2))

    # Fill empty edges
    for i in range(1, n):
        for j in range(1, m):
            del s[i][j]
            s[i].insert(j, round(max((s[i-1][j] + float(w_down[i-1][j])),
                                      s[i][j-1] + float(w_right[i][j-1])), 2))

    return s


in_path = sys.argv[1]
w_down, w_right, n, m = parse_file(in_path)
s = manhattan_tourist(w_down, w_right, n, m)

print("Knotenwert-Matrix:\n")
for row in s:
    for element in row:
        print('{0:{filler}}'.format('{:06.2f}'.format(element), filler=5), end='  ')
    print("\n")

print("Max. Score:", s[-1][-1])
