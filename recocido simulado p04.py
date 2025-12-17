import random
import math
import matplotlib.pyplot as plt
import csv
import statistics
from scipy import stats

# ===============================
# DATOS P04 (1 mochila)
# ===============================
n = 10
capacidad = 165

pesos = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
beneficios = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]

# ===============================
# FUNCIONES
# ===============================
def evaluar(asignacion):
    peso_total = sum(pesos[i] for i in range(n) if asignacion[i] == 1)
    if peso_total > capacidad:
        return -1
    return sum(beneficios[i] for i in range(n) if asignacion[i] == 1)

def vecino(asignacion):
    v = asignacion[:]
    i = random.randint(0, n - 1)
    v[i] = 1 - v[i]
    return v

def simulated_annealing(T=1000, alpha=0.60, iteraciones=1000):
    estado = [0] * n
    mejor_estado = estado[:]
    mejor_valor = evaluar(estado)

    hist_beneficio = [mejor_valor]
    hist_peso = [0]
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
        hist_peso.append(sum(pesos[i] for i in range(n) if estado[i] == 1))
        hist_temp.append(T)

        T *= alpha

    return mejor_valor, mejor_estado, hist_beneficio, hist_peso, hist_temp

# ===============================
# 30 CORRIDAS
# ===============================
corridas = 30
beneficios_corridas = []

mejor_global = -1
mejor_data = None

with open("resultados_SA_P04_1M.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Corrida",
        "Beneficio",
        "Peso",
        "Asignacion",
        "Objetos"
    ])

    print("\n========== RESULTADOS DE LAS 30 CORRIDAS ==========\n")

    for r in range(1, corridas + 1):
        opt, asign, h_ben, h_peso, h_temp = simulated_annealing()

        peso_final = sum(pesos[i] for i in range(n) if asign[i] == 1)
        objetos = [i + 1 for i in range(n) if asign[i] == 1]

        beneficios_corridas.append(opt)

        writer.writerow([
            r,
            opt,
            peso_final,
            asign,
            objetos
        ])

        print(f"Corrida {r:02d}")
        print(f"  Beneficio = {opt}")
        print(f"  Peso      = {peso_final}/{capacidad}")
        print(f"  Asignación = {asign}")
        print(f"  Objetos   = {objetos}\n")

        if opt > mejor_global:
            mejor_global = opt
            mejor_data = (opt, asign, h_ben, h_peso, h_temp)

# ===============================
# MEJOR SOLUCIÓN GLOBAL
# ===============================
opt, asign, hist_beneficio, hist_peso, hist_temp = mejor_data
objetos_finales = [i + 1 for i in range(n) if asign[i] == 1]

print("\n========== MEJOR SOLUCIÓN GLOBAL ==========")
print("Beneficio =", opt)
print("Asignación =", asign)
print("Objetos seleccionados =", objetos_finales)
print("Peso total =", sum(pesos[i] for i in range(n) if asign[i] == 1), "/", capacidad)

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

# Intervalo de confianza
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

# Normalidad
if len(set(beneficios_corridas)) > 1:
    shapiro = stats.shapiro(beneficios_corridas)
    print(f"Shapiro-Wilk p-value = {shapiro.pvalue:.4f}")
else:
    print("Shapiro-Wilk: no aplicable (resultados idénticos)")

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
plt.plot(hist_peso, marker='o')
plt.axhline(capacidad, linestyle='--', label="Capacidad")
plt.title("Peso usado vs Iteraciones (Mejor solución)")
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
plt.bar([f"Objeto {i+1}" for i in range(n)], asign)
plt.title("Objetos seleccionados en la mejor solución")
plt.ylabel("Seleccionado (1 = Sí, 0 = No)")
plt.show()
