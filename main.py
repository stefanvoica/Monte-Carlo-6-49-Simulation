import random
import numpy as np
import matplotlib.pyplot as plt

numere_frecvente = {
    1: 288, 2: 301, 3: 278, 4: 309, 5: 325, 6: 318, 7: 278, 8: 274, 9: 297, 10: 294,
    11: 271, 12: 298, 13: 307, 14: 272, 15: 283, 16: 293, 17: 297, 18: 288, 19: 269,
    20: 286, 21: 270, 22: 263, 23: 301, 24: 295, 25: 311, 26: 291, 27: 308, 28: 279,
    29: 274, 30: 282, 31: 257, 32: 281, 33: 292, 34: 277, 35: 261, 36: 318, 37: 276,
    38: 287, 39: 286, 40: 259, 41: 282, 42: 254, 43: 282, 44: 280, 45: 280, 46: 290,
    47: 261, 48: 285, 49: 259
}

suma_totala = sum(numere_frecvente.values())

raporturi_complete = {numar: valoare / suma_totala for numar, valoare in numere_frecvente.items()}

sume_partial_cumulative = {}
cumul = 0

for numar, raport in sorted(raporturi_complete.items()):
    cumul += raport
    sume_partial_cumulative[numar] = cumul

def pick_number():
    r = random.random()
    for i, cp in sume_partial_cumulative.items():
        if r <= cp:
            return i

def simulari(nr_simulari, nr_bilete, numar_minim_potriviri):
    def bilet_jucator(numar_numere=6):
        draw = set()
        while len(draw) < numar_numere:
            draw.add(pick_number())
        return draw

    def extragere_loterie(numar_numere=6):
        draw = set()
        while len(draw) < numar_numere:
            draw.add(random.randint(1, 49))
        return draw

    def extragere_azi(nr_bilete):
        set_loterie = extragere_loterie()
        k = 0
        for _ in range(nr_bilete):
            set_bilet_jucator = bilet_jucator()
            if len(set_loterie.intersection(set_bilet_jucator)) >= numar_minim_potriviri:
                k += 1
        return k

    bilete_castigatoare = []
    for _ in range(int(nr_simulari)):
        bilete_castigatoare.append(extragere_azi(nr_bilete))
    return np.array(bilete_castigatoare)

def generare_histograma(nr_simulari, nr_bilete, numar_minim_potriviri):
    print(f"Generăm histograma pentru {nr_simulari} simulări și {nr_bilete} bilete...")
    rezultate_simulare = simulari(nr_simulari, nr_bilete, numar_minim_potriviri)
    media = np.mean(rezultate_simulare)
    deviatia_std = np.std(rezultate_simulare)
    bins = np.arange(int(media - 3 * deviatia_std), int(media + 3 * deviatia_std) + 1)
    plt.hist(rezultate_simulare, bins=bins, align='left', edgecolor='black', rwidth=0.8, density=True)
    x = np.linspace(media - 3 * deviatia_std, media + 3 * deviatia_std, 1000)
    pdf = (1 / (deviatia_std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media) / deviatia_std) ** 2)
    plt.plot(x, pdf, color='red', label="Distribuție Normală")
    plt.title(f"Histogramă - {nr_simulari} simulări, {nr_bilete} bilete, {numar_minim_potriviri} potriviri")
    plt.xlabel("Număr bilete câștigătoare")
    plt.ylabel("Frecvență (densitate)")
    plt.legend()
    plt.show()

apeluri = {
    "simulare_1": (1e4, 100),
    "simulare_2": (100000, 500),
    "simulare_3": (120000, 1000)
}

cheie = "simulare_3"
parametri = apeluri[cheie]
numar_minim_potriviri = 3
generare_histograma(int(parametri[0]), parametri[1], numar_minim_potriviri)
