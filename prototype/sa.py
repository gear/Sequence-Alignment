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

def sequence_alignment(str1, str2, tmp, i=0, j=0, tracecache=None):
    if i == 0 or j == 0:
        tmp[(i,j)] = 0
        return 0
    elif (i,j) in tmp:
        return tmp[(i,j)]
    else:
        gap1 = sequence_alignment(str1, str2, tmp, i, j-1, tracecache) + GAP
        gap2 = sequence_alignment(str1, str2, tmp, i-1, j, tracecache) + GAP
        char = sequence_alignment(str1, str2, tmp, i-1, j-1, tracecache) + \
               score(str1, str2, i, j)
        vals = [char, gap1, gap2]  # Prefer char to gap
        if tracecache is not None:
            midx = np.argmax(vals)
            if 0 == midx:
                tracecache[(i,j)] = (i-1, j-1)
            elif 1 == midx:
                tracecache[(i,j)] = (i, j-1)
            elif 2 == midx:
                tracecache[(i,j)] = (i-1, j)
            else:
                raise ValueError("Undefined index.")
        tmp[(i,j)] = max(vals)
        return tmp[(i,j)]

def main():
    args = sys.argv
    str1 = args[1]
    str2 = args[2]
    cache = {}
    trace = {}
    i = len(str1)
    j = len(str2)
    sa_score = sequence_alignment(str1, str2, cache, i, j, trace)
    print("Sequence Alignment Score: {}".format(sa_score))
    aligned_str1 = ""
    aligned_str2 = ""
    while (i,j) in trace:
        (ii,jj) = trace[(i,j)]
        if (ii < i):
            aligned_str1 += str1[ii]
        else:
            aligned_str1 += '-'
        if (jj < j):
            aligned_str2 += str2[jj]
        else:
            aligned_str2 += '-'
        (i,j) = (ii,jj)
    print(aligned_str1[::-1])
    print(aligned_str2[::-1])

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
