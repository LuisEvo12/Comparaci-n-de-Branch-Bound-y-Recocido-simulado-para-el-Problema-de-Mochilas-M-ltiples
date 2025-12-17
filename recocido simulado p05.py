import random
import math
import matplotlib.pyplot as plt
import csv
import statistics
from scipy import stats

# ===============================
# DATOS P05 (2 mochilas)
# ===============================
n = 6
m = 2

capacidades = [65, 85]
beneficios = [40, 60, 30, 40, 20, 5]

pesos = [
    [40, 110],
    [60, 150],
    [30, 70],
    [40, 80],
    [20, 30],
    [5, 5]
]

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
    j = random.randint(-1, m - 1)  # -1 = no asignado
    v[i] = j
    return v

def simulated_annealing(T=1000, alpha=0.60, iteraciones=1000):
    estado = [-1] * n
    mejor_estado = estado[:]
    mejor_valor = evaluar(estado)

    hist_beneficio = [mejor_valor]
    hist_peso = [[0] * m]
    hist_temp = [T]

    while T > 1e-3:
        for _ in range(iteraciones):
            nuevo_estado = vecino(estado)
            nuevo_valor = evaluar(nuevo_estado)

            if nuevo_valor == -1:
                continue

            delta = nuevo_valor - evaluar(estado)

            if delta > 0 or random.random() < math.exp(delta / T):
                estado = nuevo_estado[:]

                if nuevo_valor > mejor_valor:
                    mejor_valor = nuevo_valor
                    mejor_estado = nuevo_estado[:]

        hist_beneficio.append(mejor_valor)
        hist_peso.append([
            sum(pesos[i][j] for i in range(n) if estado[i] == j)
            for j in range(m)
        ])
        hist_temp.append(T)

        T *= alpha

    return mejor_valor, mejor_estado, hist_beneficio, hist_peso, hist_temp

# ===============================
# 30 CORRIDAS + CSV
# ===============================
NUM_CORRIDAS = 30
beneficios_corridas = []

mejor_global = -1
mejor_data = None

with open("resultados_SA_P05.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Corrida",
        "Beneficio",
        "Asignacion",
        "Peso_M1",
        "Peso_M2"
    ])

    print("\n========== RESULTADOS DE LAS 30 CORRIDAS ==========\n")

    for k in range(1, NUM_CORRIDAS + 1):
        opt, asign, h_ben, h_peso, h_temp = simulated_annealing()
        beneficios_corridas.append(opt)

        asign_humana = [x + 1 if x != -1 else 0 for x in asign]

        pesos_finales = [
            sum(pesos[i][j] for i in range(n) if asign[i] == j)
            for j in range(m)
        ]

        writer.writerow([
            k,
            opt,
            asign_humana,
            *pesos_finales
        ])

        print(f"Corrida {k:02d}")
        print(f"  Beneficio = {opt}")
        print(f"  Asignación = {asign_humana}")

        for j in range(m):
            objs = [i + 1 for i in range(n) if asign[i] == j]
            print(f"  Mochila {j+1}: objetos {objs}, peso {pesos_finales[j]}/{capacidades[j]}")
        print()

        if opt > mejor_global:
            mejor_global = opt
            mejor_data = (opt, asign, h_ben, h_peso, h_temp)

# ===============================
# MEJOR SOLUCIÓN GLOBAL
# ===============================
opt, asign, hist_beneficio, hist_peso, hist_temp = mejor_data

print("\n========== MEJOR SOLUCIÓN GLOBAL ==========")
print("Beneficio =", opt)
print("Asignación =", [x + 1 if x != -1 else 0 for x in asign])

# ===============================
# PRUEBAS ESTADÍSTICAS
# ===============================
media = statistics.mean(beneficios_corridas)
desv = statistics.stdev(beneficios_corridas) if len(set(beneficios_corridas)) > 1 else 0
minimo = min(beneficios_corridas)
maximo = max(beneficios_corridas)

print("\n========== ESTADÍSTICAS ==========")
print(f"Media = {media:.2f}")
print(f"Desviación estándar = {desv:.2f}")
print(f"Mínimo = {minimo}")
print(f"Máximo = {maximo}")

if desv > 0:
    ic = stats.t.interval(
        0.95,
        len(beneficios_corridas) - 1,
        loc=media,
        scale=stats.sem(beneficios_corridas)
    )
    print(f"IC 95% = ({ic[0]:.2f}, {ic[1]:.2f})")
else:
    print("IC 95% = No aplicable (varianza cero)")

if len(set(beneficios_corridas)) > 1:
    shapiro = stats.shapiro(beneficios_corridas)
    print(f"Shapiro-Wilk p-value = {shapiro.pvalue:.4f}")
else:
    print("Shapiro-Wilk: no aplicable")

# ===============================
# GRÁFICOS (MEJOR SOLUCIÓN)
# ===============================
plt.figure(figsize=(10, 5))
plt.plot(hist_beneficio, marker='o')
plt.title("Beneficio vs Iteraciones (Mejor solución)")
plt.xlabel("Iteraciones / Enfriamientos")
plt.ylabel("Beneficio")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 5))
for j in range(m):
    plt.plot(
        [p[j] for p in hist_peso],
        marker='o',
        label=f"Mochila {j+1}"
    )
    plt.axhline(capacidades[j], linestyle='--')

plt.title("Peso por mochila vs Iteraciones (Mejor solución)")
plt.xlabel("Iteraciones / Enfriamientos")
plt.ylabel("Peso usado")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(hist_temp, hist_beneficio, marker='o')
plt.title("Beneficio vs Temperatura (Mejor solución)")
plt.xlabel("Temperatura")
plt.ylabel("Beneficio")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
conteo = [
    sum(1 for i in asign if i == j)
    for j in range(m)
]
plt.bar([f"Mochila {j+1}" for j in range(m)], conteo)
plt.title("Distribución final de objetos por mochila")
plt.ylabel("Cantidad de objetos")
plt.show()
