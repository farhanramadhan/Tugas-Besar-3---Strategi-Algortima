from PreProcessing import get_nbchar
import string

def kmp_fail(pattern):
    border = [0]
    k = 1

    while k < len(pattern)-1:
        j = 1
        i = k
        recLen = 0

        while j <= k+1 and i >= 1:
            prefix = pattern[0:j]
            suffix = pattern[i:k+1]

            if prefix == suffix and j > recLen:
                recLen = j
            
            j += 1
            i -= 1
        k += 1
        border += [recLen]
    return border

def kmp(text, pattern):
    j, i, conf = 0, 0, 0
    m, n = len(text), len(pattern)
    border = kmp_fail(pattern)

    if n > m:
        return 0, -1

    while i < m:
        if pattern[j] == text[i]:
            conf += 1
            if j == n-1:
                break
            i += 1
            j += 1
        elif j > 0:
            j = border[j-1]
        else:
            i += 1
    if j == n-1:
        return 100, i
    else:
        return 0, -1

def bm_preprocess(pattern, alphabet):
    last_occur = {}

    for huruf in alphabet:
        if huruf in pattern:
            i = len(pattern)-1
            while i >= 0:
                if pattern[i] == huruf:
                    last_occur[huruf] = i
                    break
                i -= 1
        else:
            last_occur[huruf] = -1
    
    return last_occur

def bm(text, pattern):
    last_occur = bm_preprocess(pattern, list(string.ascii_lowercase) + list(string.digits) + list(string.whitespace))
    n = len(text)
    m = len(pattern)

    if m > n:
        return 0, -1

    j = m-1
    i = j
    
    while (i < n):
        if (text[i] == pattern[j]):
            if j == 0:
                return 100, i
            
            i -= 1
            j -= 1
        else:
            last_occur_idx = last_occur[text[i]]
            min_list = [j, 1+last_occur_idx]
            i += m - min(min_list)
            j = m-1
        

    return 0, -1