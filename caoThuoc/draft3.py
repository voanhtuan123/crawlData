set = ["Lidocain","hydroclorid"]
merged = []
for item in set:
    if item.startswith('(') or item.endswith(')'):
        if merged:
                    merged[-1] += " " + item
        else:
                    merged.append(item)
        
    if len(set) == 2 and item == "hydroclorid":
        if merged:
            merged[-1] += " " + item
        else:
            merged.append(item)
    else:
        merged.append(item)

print(merged)