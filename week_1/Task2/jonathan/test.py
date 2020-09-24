x = {"x": 10, "y": 15}
y = {"x": 10, "y": 15}
z = { "y": 15, "x": 10,}


print(type(hash(frozenset(y.items()))))
print(hash(frozenset(x.items())))
print(hash(frozenset(z.items())))