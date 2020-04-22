from collections import Counter

def oversample_strategy(y):
    ratio = 5.5
    counted_tags = Counter(y)
    
    max_tag = max(counted_tags)
    target_stats = {}
    for key, value in counted_tags.items():
        if key == max_tag:
            target_stats = {**target_stats, **{max_tag: value}}
        else:
            max_curr_ratio =  counted_tags[max_tag] / value 
            expected = int(value * max_curr_ratio) if max_curr_ratio <= ratio else int(value * ratio)
            target_stats[key] =expected        
    return target_stats
