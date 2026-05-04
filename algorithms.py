import time

def naive_search(text, pattern):
    matches, comparisons = [], 0
    n, m = len(text), len(pattern)
    start = time.perf_counter()
    
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    
    elapsed = (time.perf_counter() - start) * 1000
    return {'matches': matches, 'time_ms': elapsed, 'comparisons': comparisons, 'space': 4}

def kmp_search(text, pattern):
    matches, comparisons = [], 0
    n, m = len(text), len(pattern)
    
    # Build LPS
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        comparisons += 1
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    
    start = time.perf_counter()
    i = j = 0
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    
    elapsed = (time.perf_counter() - start) * 1000
    return {'matches': matches, 'time_ms': elapsed, 'comparisons': comparisons, 'space': m * 4}

def rabin_karp_search(text, pattern):
    matches, comparisons = [], 0
    n, m = len(text), len(pattern)
    base, mod = 256, 101
    
    if m > n:
        return {'matches': [], 'time_ms': 0, 'comparisons': 0, 'space': 12}
    
    start = time.perf_counter()
    pattern_hash = text_hash = h = 0
    
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
        text_hash = (base * text_hash + ord(text[i])) % mod
        if i > 0:
            h = (h * base) % mod
        else:
            h = 1
    
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            match = True
            for j in range(m):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                matches.append(i)
        
        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            if text_hash < 0:
                text_hash += mod
    
    elapsed = (time.perf_counter() - start) * 1000
    return {'matches': matches, 'time_ms': elapsed, 'comparisons': comparisons, 'space': 12}

def boyer_moore_horspool_search(text, pattern):
    matches, comparisons = [], 0
    n, m = len(text), len(pattern)
    
    if m > n:
        return {'matches': [], 'time_ms': 0, 'comparisons': 0, 'space': 256 * 4}
    
    bad_char = {c: m for c in set(text)}
    for i in range(m - 1):
        bad_char[pattern[i]] = m - 1 - i
    
    start = time.perf_counter()
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0:
            comparisons += 1
            if pattern[j] != text[i + j]:
                break
            j -= 1
        
        if j < 0:
            matches.append(i)
            i += 1
        else:
            i += bad_char.get(text[i + m - 1], m)
    
    elapsed = (time.perf_counter() - start) * 1000
    return {'matches': matches, 'time_ms': elapsed, 'comparisons': comparisons, 'space': 256 * 4}
