print(str := '123456789')
print([int(line) for line in str])
bark = {"B1": "12345", "B2": "1"}
print(list(bark["B1"]))
print(all(len(list(value)) == 1 for value in bark.values()))

