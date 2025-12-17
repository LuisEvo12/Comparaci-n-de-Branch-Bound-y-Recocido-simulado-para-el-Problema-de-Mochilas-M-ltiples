import random
import math
import matplotlib.pyplot as plt

# ===============================
# DATOS DEL PROBLEMA
# ===============================
n = 5
m = 3

capacidades = [50, 50, 50]
beneficios = [60, 100, 120, 80, 30]

pesos = [
    [10, 20, 30],
    [20, 10, 20],
    [30, 30, 10],
    [10, 40, 20],
    [20, 20, 10]
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
                estado = nuevo
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
# 30 CORRIDAS
# ===============================

NUM_CORRIDAS = 30

mejor_global = -1
mejor_asignacion = None
hist_beneficio_global = None
hist_peso_global = None
hist_temp_global = None

for k in range(NUM_CORRIDAS):
    opt, asign, hist_ben, hist_peso, hist_temp = simulated_annealing()

    asign_humana = [x + 1 if x != -1 else 0 for x in asign]

    print(f"\nCorrida {k+1}")
    print(f"Beneficio = {opt}")
    print(f"Asignación por objeto = {asign_humana}")

    for j in range(m):
        objs = [i + 1 for i in range(n) if asign[i] == j]
        peso = sum(pesos[i][j] for i in range(n) if asign[i] == j)
        print(f"  Mochila {j+1}: objetos {objs}, peso {peso}/{capacidades[j]}")

    if opt > mejor_global:
        mejor_global = opt
        mejor_asignacion = asign
        hist_beneficio_global = hist_ben
        hist_peso_global = hist_peso
        hist_temp_global = hist_temp

# ===============================
# MEJOR SOLUCIÓN GLOBAL
# ===============================

asign_humana = [x + 1 if x != -1 else 0 for x in mejor_asignacion]

print("\n========== MEJOR SOLUCIÓN GLOBAL ==========")
print(f"Beneficio = {mejor_global}")
print(f"Asignación por objeto = {asign_humana}")

for j in range(m):
    objs = [i + 1 for i in range(n) if mejor_asignacion[i] == j]
    peso = sum(pesos[i][j] for i in range(n) if mejor_asignacion[i] == j)
    print(f"Mochila {j+1}: objetos {objs}, peso {peso}/{capacidades[j]}")

# ===============================
# GRAFICAS (SOLO MEJOR SOLUCIÓN)
# ===============================

plt.figure(figsize=(10,5))
plt.plot(hist_beneficio_global, marker='o')
plt.title("Beneficio vs Iteraciones (mejor solución)")
plt.xlabel("Iteraciones / Enfriamientos")
plt.ylabel("Beneficio")
plt.grid(True)
plt.show()

plt.figure(figsize=(10,5))
for j in range(m):
    plt.plot([p[j] for p in hist_peso_global], marker='o', label=f"Mochila {j+1}")
plt.title("Peso por mochila vs Iteraciones (mejor solución)")
plt.xlabel("Iteraciones / Enfriamientos")
plt.ylabel("Peso usado")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10,5))
plt.plot(hist_temp_global, hist_beneficio_global, marker='o')
plt.title("Beneficio vs Temperatura (mejor solución)")
plt.xlabel("Temperatura")
plt.ylabel("Beneficio")
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
conteo = [sum(1 for i in mejor_asignacion if i == j) for j in range(m)]
plt.bar([f"Mochila {j+1}" for j in range(m)], conteo)
plt.title("Distribución final de objetos por mochila")
plt.ylabel("Cantidad de objetos")
plt.show()
