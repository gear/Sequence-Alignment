import os
import sys
import numpy as np

# Scores
GAP = -1
MISMATCH = -1
MATCH = 2

def score(str1, str2, i, j):
    if str1[i-1] == str2[j-1]:
        return MATCH
    else:
        return MISMATCH

def sequence_alignment(str1, str2, tmp, i=0, j=0, traceback=None):
    if i == 0 or j == 0:
        return 0
    elif (i,j) in tmp:
        return tmp[(i,j)]
    else:
        gap1 = sequence_alignment(str1, str2, tmp, i, j-1) + GAP
        gap2 = sequence_alignment(str1, str2, tmp, i-1, j) + GAP
        char = sequence_alignment(str1, str2, tmp, i-1, j-1) + score(str1, str2, i, j)
        tmp[(i,j)] = max(gap1, gap2, char)
        return tmp[(i,j)]

def main():
    args = sys.argv
    str1 = args[1]
    str2 = args[2]
    cache = {}
    print(sequence_alignment(str1, str2, cache, len(str1), len(str2)))

def test():

    print("Test-1: ATGC - AGAC")
    str1 = "ATGC"
    str2 = "AGAC"
    assert sequence_alignment(str1, str2, {}, len(str1), len(str2)) == 4
    print("Test-1 PASSED")

    print("Test-2: ATTGCTCGTTGGA - AAAACCGTAA")
    str1 = "ATTGCTCGTTGGA"
    str2 = "AAAACCGTAA"
    assert sequence_alignment(str1, str2, {}, len(str1), len(str2)) == 5

if __name__ == '__main__':
    main()
