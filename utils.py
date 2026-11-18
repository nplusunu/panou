# utils.py

zile_saptamana_ro = {
    0: "Luni", 1: "Marti", 2: "Miercuri", 3: "Joi",
    4: "Vineri", 5: "Sambata", 6: "Duminica"
}

luni_ro = {
    1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie",
    5: "Mai", 6: "Iunie", 7: "Iulie", 8: "August",
    9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"
}

zile_saptamana = [
    "Luni", "Marti", "Miercuri", "Joi", "Vineri", "Sambata", "Duminica"
]

def salut(ora):
    if ora < 12:
        return "Buna dimineata!"
    elif ora < 18:
        return "Buna ziua!"
    else:
        return "Buna seara!"