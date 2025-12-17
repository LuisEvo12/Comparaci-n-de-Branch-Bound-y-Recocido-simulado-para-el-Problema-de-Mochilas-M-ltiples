import heapq

# ===============================
# DATOS P05
# ===============================
n = 6  # número de objetos
m = 2  # número de mochilas
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
# CLASE NODO PARA BRANCH & BOUND
# ===============================
class Nodo:
    def __init__(self, nivel, beneficio, capacidad_restante, asignacion):
        self.nivel = nivel
        self.beneficio = beneficio
        self.capacidad_restante = capacidad_restante[:]
        self.asignacion = asignacion[:]
        self.cota = 0

    def __lt__(self, otro):
        # heapq por defecto es min-heap, usamos cota invertida para max-heap
        return self.cota > otro.cota

# ===============================
# FUNCION DE COTA SUPERIOR
# ===============================
def calcular_cota(nodo):
    beneficio_estimado = nodo.beneficio
    capacidad = nodo.capacidad_restante[:]

    for i in range(nodo.nivel, n):
        # Intentar colocar objeto i en alguna mochila disponible
        for j in range(m):
            if pesos[i][j] <= capacidad[j]:
                beneficio_estimado += beneficios[i]
                capacidad[j] -= pesos[i][j]
                break  # cada objeto solo puede ir a una mochila
    return beneficio_estimado

# ===============================
# BRANCH & BOUND EXACTO
# ===============================
def branch_and_bound_exacto():
    mejor_beneficio = 0
    mejor_asignacion = [-1]*n

    root = Nodo(0, 0, capacidades, [-1]*n)
    root.cota = calcular_cota(root)
    pq = [root]

    while pq:
        nodo = heapq.heappop(pq)

        # Podar nodos cuya cota no supere el mejor beneficio actual
        if nodo.cota <= mejor_beneficio:
            continue

        # Si llegamos al último nivel, actualizar mejor solución
        if nodo.nivel == n:
            if nodo.beneficio > mejor_beneficio:
                mejor_beneficio = nodo.beneficio
                mejor_asignacion = nodo.asignacion[:]
            continue

        i = nodo.nivel

        # PROBAR ASIGNAR OBJETO i A CADA MOCHILA
        for j in range(m):
            if pesos[i][j] <= nodo.capacidad_restante[j]:
                hijo = Nodo(
                    nivel=i+1,
                    beneficio=nodo.beneficio + beneficios[i],
                    capacidad_restante=nodo.capacidad_restante[:],
                    asignacion=nodo.asignacion[:]
                )
                hijo.capacidad_restante[j] -= pesos[i][j]
                hijo.asignacion[i] = j
                hijo.cota = calcular_cota(hijo)
                if hijo.cota > mejor_beneficio:
                    heapq.heappush(pq, hijo)

        # PROBAR NO ASIGNAR OBJETO i
        hijo_no = Nodo(
            nivel=i+1,
            beneficio=nodo.beneficio,
            capacidad_restante=nodo.capacidad_restante[:],
            asignacion=nodo.asignacion[:]
        )
        hijo_no.asignacion[i] = -1
        hijo_no.cota = calcular_cota(hijo_no)
        if hijo_no.cota > mejor_beneficio:
            heapq.heappush(pq, hijo_no)

    return mejor_beneficio, mejor_asignacion

# ===============================
# EJECUCIÓN
# ===============================
opt, asign = branch_and_bound_exacto()
# Convertir asignación a 1-based para imprimir
asign_1 = [x+1 if x != -1 else 0 for x in asign]

print("\nBeneficio óptimo =", opt)
print("Asignación por objeto =", asign_1)

print("\nResumen por mochila:")
for j in range(m):
    objs = [i+1 for i in range(n) if asign[i] == j]
    peso = sum(pesos[i][j] for i in range(n) if asign[i] == j)
    print(f"  Mochila {j+1}: objetos {objs}, peso usado {peso}/{capacidades[j]}")
