def recommend_algorithm(n, m, text_type, expected_matches):
    recommendations = []
    
    # Analyze characteristics
    ratio = n / m if m > 0 else 0
    
    if text_type == "repetitive" or expected_matches == "many":
        recommendations.append({
            "algorithm": "KMP",
            "score": 95,
            "reason": "Optimal for repetitive text with many matches. Linear time O(n+m) guaranteed."
        })
        recommendations.append({
            "algorithm": "Boyer-Moore-Horspool",
            "score": 70,
            "reason": "Good for longer patterns but may not skip as much in repetitive text."
        })
        recommendations.append({
            "algorithm": "Rabin-Karp",
            "score": 60,
            "reason": "Decent performance but hash collisions may occur in repetitive text."
        })
        recommendations.append({
            "algorithm": "Naive",
            "score": 30,
            "reason": "Poor choice - O(n×m) worst case likely with repetitive patterns."
        })
    elif m > 10 and ratio > 100:
        recommendations.append({
            "algorithm": "Boyer-Moore-Horspool",
            "score": 95,
            "reason": "Best for long patterns in large text. Can skip many positions."
        })
        recommendations.append({
            "algorithm": "KMP",
            "score": 85,
            "reason": "Reliable linear time performance for any input."
        })
        recommendations.append({
            "algorithm": "Rabin-Karp",
            "score": 75,
            "reason": "Good average case but preprocessing overhead for long patterns."
        })
        recommendations.append({
            "algorithm": "Naive",
            "score": 40,
            "reason": "Simple but inefficient for long patterns."
        })
    elif m <= 3:
        recommendations.append({
            "algorithm": "Naive",
            "score": 85,
            "reason": "Simple and efficient for very short patterns. Low overhead."
        })
        recommendations.append({
            "algorithm": "Boyer-Moore-Horspool",
            "score": 80,
            "reason": "Good performance even with short patterns."
        })
        recommendations.append({
            "algorithm": "KMP",
            "score": 70,
            "reason": "Preprocessing overhead may not be worth it for short patterns."
        })
        recommendations.append({
            "algorithm": "Rabin-Karp",
            "score": 65,
            "reason": "Hash computation overhead for short patterns."
        })
    else:
        recommendations.append({
            "algorithm": "KMP",
            "score": 90,
            "reason": "Balanced choice with guaranteed O(n+m) performance."
        })
        recommendations.append({
            "algorithm": "Boyer-Moore-Horspool",
            "score": 85,
            "reason": "Good average case performance for medium patterns."
        })
        recommendations.append({
            "algorithm": "Rabin-Karp",
            "score": 75,
            "reason": "Decent performance with low space usage."
        })
        recommendations.append({
            "algorithm": "Naive",
            "score": 50,
            "reason": "Simple but not optimal for medium-sized patterns."
        })
    
    return sorted(recommendations, key=lambda x: x['score'], reverse=True)

def calculate_statistics(df):
    stats = df.groupby(['Algorithm', 'Text Type', 'n', 'm']).agg({
        'Time (ms)': ['mean', 'median', 'std', 'min', 'max'],
        'Comparisons': ['mean', 'median', 'std', 'min', 'max']
    }).reset_index()
    
    stats.columns = ['Algorithm', 'Text Type', 'n', 'm', 
                     'Time Mean', 'Time Median', 'Time Std', 'Time Min', 'Time Max',
                     'Comp Mean', 'Comp Median', 'Comp Std', 'Comp Min', 'Comp Max']
    return stats
