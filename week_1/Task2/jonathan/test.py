x = {"x": 10, "y": 15}
y = {"x": 10, "y": 15, "z": 15}

print(hash(frozenset(y.items())))
print(hash(frozenset(x.items())))