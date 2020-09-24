x = {"x": 10, "y": 15}
z = { "y": 15, "x": 10,}
m = x.copy()


print(hash(frozenset(x.items())))
print(hash(frozenset(z.items())))
y = {"x": 10, "y": 15}
print(hash(frozenset(y.items())))
print(hash(frozenset(m.items())))

