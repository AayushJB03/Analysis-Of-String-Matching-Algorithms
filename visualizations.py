def naive_steps(text, pattern):
    n, m = len(text), len(pattern)
    comparisons = 0
    for i in range(n - m + 1):
        for j in range(m):
            comparisons += 1
            yield {
                'step': comparisons,
                'text_pos': i,
                'pattern_pos': j,
                'comparing': (i + j, j),
                'match': text[i + j] == pattern[j],
                'message': f"Comparing text[{i+j}]='{text[i+j]}' with pattern[{j}]='{pattern[j]}'",
                'found_match': False
            }
            if text[i + j] != pattern[j]:
                yield {
                    'step': comparisons,
                    'text_pos': i,
                    'pattern_pos': j,
                    'comparing': None,
                    'match': False,
                    'message': f"Mismatch! Shifting pattern by 1 position",
                    'found_match': False
                }
                break
        else:
            yield {
                'step': comparisons,
                'text_pos': i,
                'pattern_pos': m,
                'comparing': None,
                'match': True,
                'message': f"✅ Match found at position {i}!",
                'found_match': True
            }

def kmp_steps(text, pattern):
    n, m = len(text), len(pattern)
    
    # Build LPS
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    
    yield {
        'step': 0,
        'text_pos': 0,
        'pattern_pos': 0,
        'comparing': None,
        'match': None,
        'message': f"LPS Array computed: {lps}",
        'found_match': False,
        'lps': lps
    }
    
    i = j = 0
    step = 0
    while i < n:
        step += 1
        if pattern[j] == text[i]:
            yield {
                'step': step,
                'text_pos': i - j,
                'pattern_pos': j,
                'comparing': (i, j),
                'match': True,
                'message': f"Match: text[{i}]='{text[i]}' == pattern[{j}]='{pattern[j]}'",
                'found_match': False,
                'lps': lps
            }
            i += 1
            j += 1
            if j == m:
                yield {
                    'step': step,
                    'text_pos': i - j,
                    'pattern_pos': j,
                    'comparing': None,
                    'match': True,
                    'message': f"✅ Match found at position {i - j}! Using LPS to continue",
                    'found_match': True,
                    'lps': lps
                }
                j = lps[j - 1]
        else:
            yield {
                'step': step,
                'text_pos': i - j,
                'pattern_pos': j,
                'comparing': (i, j),
                'match': False,
                'message': f"Mismatch: text[{i}]='{text[i]}' != pattern[{j}]='{pattern[j]}'. Using LPS[{j}]={lps[j-1] if j > 0 else 0}",
                'found_match': False,
                'lps': lps
            }
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

def rabin_karp_steps(text, pattern):
    n, m = len(text), len(pattern)
    base, mod = 256, 101
    
    pattern_hash = text_hash = h = 0
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
        text_hash = (base * text_hash + ord(text[i])) % mod
        if i > 0:
            h = (h * base) % mod
        else:
            h = 1
    
    yield {
        'step': 0,
        'text_pos': 0,
        'pattern_pos': 0,
        'comparing': None,
        'match': None,
        'message': f"Pattern hash: {pattern_hash}, Initial window hash: {text_hash}",
        'found_match': False,
        'pattern_hash': pattern_hash,
        'text_hash': text_hash
    }
    
    step = 0
    for i in range(n - m + 1):
        step += 1
        if pattern_hash == text_hash:
            yield {
                'step': step,
                'text_pos': i,
                'pattern_pos': 0,
                'comparing': None,
                'match': None,
                'message': f"Hash match! Verifying character by character...",
                'found_match': False,
                'pattern_hash': pattern_hash,
                'text_hash': text_hash
            }
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                yield {
                    'step': step,
                    'text_pos': i,
                    'pattern_pos': m,
                    'comparing': None,
                    'match': True,
                    'message': f"✅ Match found at position {i}!",
                    'found_match': True,
                    'pattern_hash': pattern_hash,
                    'text_hash': text_hash
                }
            else:
                yield {
                    'step': step,
                    'text_pos': i,
                    'pattern_pos': 0,
                    'comparing': None,
                    'match': False,
                    'message': f"False positive - hash collision!",
                    'found_match': False,
                    'pattern_hash': pattern_hash,
                    'text_hash': text_hash
                }
        
        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            if text_hash < 0:
                text_hash += mod
            yield {
                'step': step,
                'text_pos': i + 1,
                'pattern_pos': 0,
                'comparing': None,
                'match': None,
                'message': f"Rolling hash: new hash = {text_hash}",
                'found_match': False,
                'pattern_hash': pattern_hash,
                'text_hash': text_hash
            }

def bmh_steps(text, pattern):
    n, m = len(text), len(pattern)
    
    bad_char = {c: m for c in set(text)}
    for i in range(m - 1):
        bad_char[pattern[i]] = m - 1 - i
    
    yield {
        'step': 0,
        'text_pos': 0,
        'pattern_pos': 0,
        'comparing': None,
        'match': None,
        'message': f"Bad character table computed",
        'found_match': False,
        'bad_char': bad_char
    }
    
    i = 0
    step = 0
    while i <= n - m:
        j = m - 1
        while j >= 0:
            step += 1
            yield {
                'step': step,
                'text_pos': i,
                'pattern_pos': j,
                'comparing': (i + j, j),
                'match': pattern[j] == text[i + j],
                'message': f"Comparing text[{i+j}]='{text[i+j]}' with pattern[{j}]='{pattern[j]}' (right to left)",
                'found_match': False,
                'bad_char': bad_char
            }
            if pattern[j] != text[i + j]:
                shift = bad_char.get(text[i + m - 1], m)
                yield {
                    'step': step,
                    'text_pos': i,
                    'pattern_pos': j,
                    'comparing': None,
                    'match': False,
                    'message': f"Mismatch! Shifting by {shift} using bad char '{text[i + m - 1]}'",
                    'found_match': False,
                    'bad_char': bad_char
                }
                break
            j -= 1
        
        if j < 0:
            yield {
                'step': step,
                'text_pos': i,
                'pattern_pos': 0,
                'comparing': None,
                'match': True,
                'message': f"✅ Match found at position {i}!",
                'found_match': True,
                'bad_char': bad_char
            }
            i += 1
        else:
            i += bad_char.get(text[i + m - 1], m)

def render_visualization(text, pattern, state):
    """Render the current state of pattern matching"""
    n, m = len(text), len(pattern)
    text_pos = state.get('text_pos', 0)
    comparing = state.get('comparing', None)
    found_match = state.get('found_match', False)
    
    # Create HTML visualization
    html = '<div style="font-family: monospace; font-size: 16px; line-height: 2;">'
    
    # Render text
    html += '<div><b>Text:</b> '
    for i, char in enumerate(text):
        color = '#ddd'
        if comparing and i == comparing[0]:
            color = '#fbbf24' if state['match'] else '#ef4444'
        elif found_match and text_pos <= i < text_pos + m:
            color = '#10b981'
        html += f'<span style="background-color: {color}; padding: 2px 6px; margin: 1px; border-radius: 3px;">{char}</span>'
    html += '</div>'
    
    # Render pattern alignment
    html += '<div style="margin-top: 10px;"><b>Pattern:</b> '
    html += '&nbsp;' * 10 * text_pos
    for j, char in enumerate(pattern):
        color = '#ddd'
        if comparing and j == comparing[1]:
            color = '#fbbf24' if state['match'] else '#ef4444'
        elif found_match:
            color = '#10b981'
        html += f'<span style="background-color: {color}; padding: 2px 6px; margin: 1px; border-radius: 3px;">{char}</span>'
    html += '</div></div>'
    
    return html
