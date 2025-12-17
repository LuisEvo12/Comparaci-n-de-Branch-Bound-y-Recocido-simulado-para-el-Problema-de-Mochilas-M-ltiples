import random
import math
import matplotlib.pyplot as plt
import csv
import statistics
from scipy import stats

# ===============================
# DATOS P03 OR-LIBRARY
# ===============================
n = 10
m = 4
capacidades = [31, 37, 48, 152]

pesos_base = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
beneficios = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]

pesos = [[p] * m for p in pesos_base]

# ===============================
# FUNCIONES
# ===============================
def evaluar(asignacion):
    for j in range(m):
        peso = sum(pesos[i][j] for i in range(n) if asignacion[i] == j)
        if peso > capacidades[j]:
            return -1
    return sum(beneficios[i] for i in range(n) if asignacion[i] != -1)

def vecino(asignacion):
    v = asignacion[:]
    i = random.randint(0, n - 1)
    j = random.randint(-1, m - 1)
    v[i] = j
    return v

def simulated_annealing(T=1000, alpha=0.60, iteraciones=1000):
    estado = [-1] * n
    mejor_estado = estado[:]
    mejor_valor = evaluar(estado)

    historia_beneficio = [mejor_valor]
    historia_peso = [[0] * m]
    historia_temperatura = [T]

    while T > 1e-3:
        for _ in range(iteraciones):
            nuevo = vecino(estado)
            nuevo_valor = evaluar(nuevo)

            if nuevo_valor == -1:
                continue

            delta = nuevo_valor - evaluar(estado)

            if delta > 0 or random.random() < math.exp(delta / T):
                estado = nuevo[:]
                if nuevo_valor > mejor_valor:
                    mejor_valor = nuevo_valor
                    mejor_estado = nuevo[:]

        historia_beneficio.append(mejor_valor)
        historia_peso.append([
            sum(pesos[i][j] for i in range(n) if estado[i] == j)
            for j in range(m)
        ])
        historia_temperatura.append(T)

        T *= alpha

    return mejor_valor, mejor_estado, historia_beneficio, historia_peso, historia_temperatura

# ===============================
# 50 CORRIDAS + CSV
# ===============================
NUM_CORRIDAS = 30
beneficios_corridas = []

with open("resultados_SA_P03.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Corrida", "Beneficio",
        "Asignacion",
        "Peso_M1", "Peso_M2", "Peso_M3", "Peso_M4"
    ])

    mejor_global = -1
    mejor_asignacion = None
    hist_beneficio_global = None
    hist_peso_global = None
    hist_temp_global = None

    for k in range(NUM_CORRIDAS):
        opt, asign, hist_ben, hist_peso, hist_temp = simulated_annealing()
        beneficios_corridas.append(opt)

        asign_humana = [x + 1 if x != -1 else 0 for x in asign]

        pesos_finales = [
            sum(pesos[i][j] for i in range(n) if asign[i] == j)
            for j in range(m)
        ]

        writer.writerow([
            k + 1,
            opt,
            asign_humana,
            *pesos_finales
        ])

        print(f"\nCorrida {k+1}")
        print(f"Beneficio = {opt}")
        print(f"Asignación = {asign_humana}")

        for j in range(m):
            objs = [i + 1 for i in range(n) if asign[i] == j]
            print(f"  Mochila {j+1}: objetos {objs}, peso {pesos_finales[j]}/{capacidades[j]}")

        if opt > mejor_global:
            mejor_global = opt
            mejor_asignacion = asign
            hist_beneficio_global = hist_ben
            hist_peso_global = hist_peso
            hist_temp_global = hist_temp

# ===============================
# MEJOR SOLUCIÓN GLOBAL
# ===============================
print("\n========== MEJOR SOLUCIÓN GLOBAL ==========")
print(f"Beneficio = {mejor_global}")
print(f"Asignación = {[x + 1 if x != -1 else 0 for x in mejor_asignacion]}")

# ===============================
# PRUEBAS ESTADÍSTICAS
# ===============================
media = statistics.mean(beneficios_corridas)
desv = statistics.stdev(beneficios_corridas)
minimo = min(beneficios_corridas)
maximo = max(beneficios_corridas)

print("\n========== ESTADÍSTICAS ==========")
print(f"Media = {media:.2f}")
print(f"Desviación estándar = {desv:.2f}")
print(f"Mínimo = {minimo}")
print(f"Máximo = {maximo}")

# Intervalo de confianza 95%
ic = stats.t.interval(
    0.95,
    len(beneficios_corridas) - 1,
    loc=media,
    scale=stats.sem(beneficios_corridas)
)

print(f"IC 95% = ({ic[0]:.2f}, {ic[1]:.2f})")

# Prueba de normalidad
shapiro = stats.shapiro(beneficios_corridas)
print(f"Shapiro-Wilk p-value = {shapiro.pvalue:.4f}")
