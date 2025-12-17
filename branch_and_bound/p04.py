import heapq

# ============================
# DATOS P04
# ============================
n = 10
capacidad_total = 165

pesos =     [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
beneficios = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]

# ============================
# CLASE NODO
# ============================

class Nodo:
    def __init__(self, nivel, beneficio, peso, asignacion):
        self.nivel = nivel
        self.beneficio = beneficio
        self.peso = peso
        self.asignacion = asignacion[:]
        self.cota = 0

    def __lt__(self, other):
        return self.cota > other.cota  # max-heap simulado


# ============================
# CALCULAR COTA FRACCIONAL
# ============================

def calcular_cota(nodo):
    if nodo.peso > capacidad_total:
        return -1

    beneficio = nodo.beneficio
    peso = nodo.peso

    # Llenamos con objetos restantes usando knapsack fraccional
    for i in range(nodo.nivel, n):
        if peso + pesos[i] <= capacidad_total:
            beneficio += beneficios[i]
            peso += pesos[i]
        else:
            restante = capacidad_total - peso
            beneficio += beneficios[i] * (restante / pesos[i])
            break

    return beneficio


# ============================
# BRANCH AND BOUND
# ============================

def branch_and_bound():
    mejor_beneficio = 0
    mejor_asignacion = None

    raiz = Nodo(0, 0, 0, [0]*n)
    raiz.cota = calcular_cota(raiz)

    pq = [raiz]

    while pq:
        nodo = heapq.heappop(pq)

        if nodo.cota < mejor_beneficio:
            continue

        if nodo.nivel == n:
            if nodo.beneficio > mejor_beneficio:
                mejor_beneficio = nodo.beneficio
                mejor_asignacion = nodo.asignacion[:]
            continue

        i = nodo.nivel

        # Opción 1: Tomar objeto i
        hijo_tomar = Nodo(
            i+1,
            nodo.beneficio + beneficios[i],
            nodo.peso + pesos[i],
            nodo.asignacion
        )
        hijo_tomar.asignacion = nodo.asignacion[:]
        hijo_tomar.asignacion[i] = 1
        hijo_tomar.cota = calcular_cota(hijo_tomar)

        if hijo_tomar.cota >= mejor_beneficio:
            heapq.heappush(pq, hijo_tomar)

        # Opción 2: No tomar objeto i
        hijo_no = Nodo(
            i+1,
            nodo.beneficio,
            nodo.peso,
            nodo.asignacion
        )
        hijo_no.asignacion = nodo.asignacion[:]
        hijo_no.asignacion[i] = 0
        hijo_no.cota = calcular_cota(hijo_no)

        if hijo_no.cota >= mejor_beneficio:
            heapq.heappush(pq, hijo_no)

    return mejor_beneficio, mejor_asignacion


# ============================
# EJECUTAR
# ============================

opt, asign = branch_and_bound()

print("\n========= RESULTADO P04 =========")
print("Beneficio óptimo =", opt)
print("Asignación binaria =", asign)

peso_total = sum(pesos[i] for i in range(n) if asign[i] == 1)
objetos = [i+1 for i in range(n) if asign[i] == 1]

print("Objetos seleccionados:", objetos)
print("Peso total usado:", peso_total, "/", capacidad_total)
