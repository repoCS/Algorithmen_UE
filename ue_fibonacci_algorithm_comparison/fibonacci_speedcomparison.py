#!/usr/bin/env python3

'''
Algorithmen Übungen - Clemens Spielvogel
Vergleich von zwei Algorithmen zur Berechnung von Fibonacci Zahlen
'''

import sys
from datetime import datetime
import subprocess

# Implementierung der Algorithmen
def RecursiveFibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        a = RecursiveFibonacci(n - 1)
        b = RecursiveFibonacci(n - 2)
        return a + b


def LookupFibonacci(n):
    digits = [1, 1]

    for i in range(2, n):
        digits += [digits[i-1] + digits[i-2]]

    return digits[-1]


# Prüfen der Laufzeiten
def CompareSpeed(n,  func1, func2):
    global total_time1
    global total_time2

    # Initiale Zeitberechnung entfernt Bias bei erstmaliger Berechnung via datetime.now()
    datetime.now()

    start = datetime.now()
    num1 = func1(n)
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
    speed_output = CompareSpeed(i, RecursiveFibonacci, LookupFibonacci)

    # Bash Output
    print("{0[0]}\t{0[1]}\t\t{0[2]}\t{0[3]}".format(speed_output))

    # Erstellen des R-Inputs
    secs1 = speed_output[2].total_seconds()
    secs2 = speed_output[3].total_seconds()
    r_input.write("{0[0]},{1:.6f},{2:.6f}\n".format(speed_output, secs1, secs2))

print("Total time:     \t{}\t{}".format(total_time1, total_time2))
r_input.close()

# Erstellung und Oeffnen der Grafik
subprocess.call(["/usr/bin/Rscript", "--vanilla", "create_linechart.R"])
subprocess.call(["xdg-open", "Fibonacci_algorithm_comparison.png"])
