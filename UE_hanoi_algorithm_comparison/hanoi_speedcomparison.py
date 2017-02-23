#!/usr/bin/env python3

import sys
from datetime import datetime
import subprocess

def RecursiveHanoi(n, fr, to):
    un = 6 - fr - to
    if n == 1:
        print("Moving disk from tower {} to tower {}.".format(fr, to))
    else:
        RecursiveHanoi(n - 1, fr, un)
        RecursiveHanoi(1, fr, to)
        RecursiveHanoi(n - 1, un, to)


def NonRecursiveHanoi(n):
    def move(start, end, cycle):
        print("Moving disk from tower {} to tower {}.".format(start + 1, end + 1))
        cycle += 1
        return cycle

    if n % 2 == 0:
        a, b, c = 0, 1, 2
    else:
        a, b, c = 0, 2, 1

    cycle = 1
    while cycle != 2 ** n:
        for set in [[a, b], [a, c], [b, c], [a, b], [c, a], [c, b],
                    [a, b], [a, c], [b, c], [b, a], [c, a], [b, c]]:
            cycle = move(set[0], set[1], cycle)
            if cycle == 2 ** n:
                break


# Prüfen der Laufzeiten
def CompareSpeed(n,  func1, func2):
    global total_time1
    global total_time2

    # Initiale Zeitberechnung entfernt Bias bei erstmaliger Berechnung via datetime.now()
    datetime.now()

    start = datetime.now()
    num1 = func1(n, 1, 3)
    end = datetime.now()
    speed1 = end - start

    start = datetime.now()
    num2 = func2(n)
    end = datetime.now()
    speed2 = end - start

    try:
        total_time1 += speed1
        total_time2 += speed2
    except:
        total_time1 = speed1
        total_time2 = speed2

    # Ueberpruefen der Ergebiskonsistenz
    if num1 == num2:
        return [n, num1, speed1, speed2]
    else:
        print("Calculation error!")


n = int(sys.argv[1])
r_input = open("r_input.csv", "w")

print("n  Fibonacci number     t(Recursive)    t(Lookup table)   (times in h:m:s)")

for i in range(1, n + 1):
    speed_output = CompareSpeed(i, RecursiveHanoi, NonRecursiveHanoi)

    # Bash Output
    print("{0[0]}\t{0[1]}\t\t{0[2]}\t{0[3]}".format(speed_output))

    # Erstellen des R-Inputs
    secs1 = speed_output[2].total_seconds()
    secs2 = speed_output[3].total_seconds()
    r_input.write("{0[0]},{1:.6f},{2:.6f}\n".format(speed_output, secs1, secs2))

print("Total time:     \t{}\t{}".format(total_time1, total_time2))
r_input.close()

# Erstellung und Oeffnen der Grafik
subprocess.call(["/usr/bin/Rscript", "--vanilla", "create_linechart_hanoi.R"])
subprocess.call(["xdg-open", "Hanoi_algorithm_comparison.png"])
