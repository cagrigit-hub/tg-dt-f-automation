from collections import defaultdict


from collections import defaultdict

map = defaultdict(list)


for i in range(1, 100):
    divider = 0
    if i > 10:
        divider = i % 10
    map[divider].append(divider * i)


liste = []
for i in map:
    liste.append({i: map[i]})

print(liste)