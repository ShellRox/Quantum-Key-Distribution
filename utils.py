def validate(shared_key, sub_shared_key, min_shared_percent):
    if len(sub_shared_key) > 0 and len(shared_key) > len(sub_shared_key):
        i = 0
        count = 0
        decision = 0
        while i < len(sub_shared_key):
            if sub_shared_key[i] == shared_key[i]:
                count += 1
            i += 1
        if count >= min_shared_percent:
            decision = 1
        else:
            decision = 0
        return decision    
    else:
        return decision
        print("Error")
