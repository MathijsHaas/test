""" testing list comprehension"""
x = 0
y = 0
lijst = []

for punt in range(7):
    lijst.append((x, y))
    x += 1
    y += 2

print(lijst)

for punt in lijst:
    lijst[punt] = 0

print(lijst)
