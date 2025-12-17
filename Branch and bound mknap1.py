import heapq

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

class Nodo:
    def __init__(self, nivel, beneficio, capacidad_restante, asignacion):
        self.nivel = nivel
        self.beneficio = beneficio
        self.capacidad_restante = capacidad_restante[:]
        self.asignacion = asignacion[:]
        self.cota = 0

    def __lt__(self, other):
        return self.cota > other.cota


def imprimir_nodo(prefix, nodo):
    print(prefix + f"[Nivel {nodo.nivel}] Benef={nodo.beneficio} Cota={nodo.cota} "
          f"Caps={nodo.capacidad_restante} Asig={nodo.asignacion}")


# Cota fraccional aproximada
def calcular_cota(nodo):
    beneficio_actual = nodo.beneficio
    capacidad = nodo.capacidad_restante[:]

    for i in range(nodo.nivel, n):
        min_j = -1
        min_peso = float('inf')
        for j in range(m):
            if pesos[i][j] <= capacidad[j] and pesos[i][j] < min_peso:
                min_j = j
                min_peso = pesos[i][j]
        if min_j != -1:
            beneficio_actual += beneficios[i]
            capacidad[min_j] -= pesos[i][min_j]
    return beneficio_actual


def branch_and_bound_con_arbol():
    mejor_beneficio = 0
    mejor_asignacion = None

    root = Nodo(0, 0, capacidades, [-1] * n)
    root.cota = calcular_cota(root)
    pq = [root]

    imprimir_nodo("", root)

    while pq:
        nodo = heapq.heappop(pq)

        if nodo.cota <= mejor_beneficio:
            continue

        if nodo.nivel == n:
            if nodo.beneficio > mejor_beneficio:
                mejor_beneficio = nodo.beneficio
                mejor_asignacion = nodo.asignacion[:]
            continue

        i = nodo.nivel
        indent = "  " * nodo.nivel

        for j in range(m):
            if pesos[i][j] <= nodo.capacidad_restante[j]:
                hijo = Nodo(
                    i + 1,
                    nodo.beneficio + beneficios[i],
                    nodo.capacidad_restante,
                    nodo.asignacion
                )
                hijo.capacidad_restante = nodo.capacidad_restante[:]
                hijo.capacidad_restante[j] -= pesos[i][j]
                hijo.asignacion = nodo.asignacion[:]
                hijo.asignacion[i] = j

                hijo.cota = calcular_cota(hijo)

                imprimir_nodo(indent, hijo)

                if hijo.cota > mejor_beneficio:
                    heapq.heappush(pq, hijo)

        # Hijo NO tomar objeto
        hijo_no = Nodo(
            i + 1,
            nodo.beneficio,
            nodo.capacidad_restante[:],
            nodo.asignacion[:]
        )
        hijo_no.asignacion[i] = -1
        hijo_no.cota = calcular_cota(hijo_no)

        imprimir_nodo(indent, hijo_no)

        if hijo_no.cota > mejor_beneficio:
            heapq.heappush(pq, hijo_no)

    return mejor_beneficio, mejor_asignacion


# Ejecutar versión con árbol
opt, asign = branch_and_bound_con_arbol()

asign_1 = [x+1 if x != -1 else 0 for x in asign]

print("\nBeneficio óptimo =", opt)
print("Asignación por objeto =", asign_1)

for j in range(m):
    objs = [i+1 for i in range(n) if asign[i] == j]
    peso = sum(pesos[i][j] for i in range(n) if asign[i] == j)
    print(f"Mochila {j+1}: objetos {objs}, peso usado {peso}/{capacidades[j]}")
