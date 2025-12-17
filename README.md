# Comparación de Branch & Bound y Recocido Simulado para el Problema de las Mochilas Múltiples

Este repositorio contiene el **código, instancias y resultados experimentales** asociados al artículo:

> **Comparación de Branch & Bound y Recocido Simulado para el Problema de las Mochilas Múltiples**
> *Lucia Francisco Bautista, Luis Eduardo Villanueva Oliver*
> Maestría en Inteligencia Artificial – IIIA
> Universidad Veracruzana

##  Resumen

El Problema de las Mochilas Múltiples (*Multiple Knapsack Problem*, MKP) es un problema clásico de optimización combinatoria clasificado como **NP-hard**, cuyo objetivo es maximizar el beneficio total al asignar objetos a múltiples mochilas con capacidades limitadas.

En este trabajo se implementan y comparan dos enfoques representativos:

* **Branch and Bound (B&B)**: método exacto que garantiza la solución óptima mediante poda inteligente del espacio de búsqueda.
* **Recocido Simulado (Simulated Annealing, SA)**: metaheurística estocástica capaz de obtener soluciones óptimas o cercanas al óptimo con menor costo computacional, especialmente en instancias más complejas.

Los resultados muestran que B&B es adecuado para instancias pequeñas y medianas, mientras que el Recocido Simulado presenta mejor **escalabilidad** en problemas de mayor tamaño.

##  Estructura del repositorio

```
├── branch_and_bound/
│   ├── mknap1/
│   ├── p03/
│   ├── p04/
│   └── p05/
├── Recocido_simulado/
│   ├── mknap1/
│   ├── p03/
│   ├── p04/
│   └── p05/
├── instancias/
│   ├── mknap1.dat
│   ├── p03.dat
│   ├── p04.dat
│   └── p05.dat
├── resultados/
│   ├── mknap1/
│   ├── p03/
│   ├── p04/
│   └── p05/
└── README.md
```

* Cada carpeta de algoritmo contiene la implementación específica **por instancia**.
* `instances/` incluye las bases de datos utilizadas en los experimentos.
* `results/` almacena tablas y gráficas generadas durante el análisis.

##  Instancias utilizadas

Se consideran cuatro instancias clásicas:

| Instancia | Tipo | Mochilas | Capacidades       | Objetos |
| --------- | ---- | -------- | ----------------- | ------- |
| MKNAP1    | MKP  | 3        | [50, 50, 50]      | 5       |
| P03       | MKP  | 4        | [31, 37, 48, 152] | 10      |
| P04       | 0–1  | 1        | [165]             | 10      |
| P05       | MKP  | 2        | [65, 85]          | 6       |

Las instancias P03, P04 y P05 provienen del repositorio público mantenido por **John Burkardt**, ampliamente utilizado en la literatura de optimización.

## 🧪 Metodología experimental

* **Branch and Bound** se utiliza como método exacto para obtener soluciones óptimas.
* **Recocido Simulado** se ejecuta con **30 corridas independientes por instancia**.
* Parámetros de SA:

  * Temperatura inicial: `T0 = 1000`
  * Factor de enfriamiento: `α = 0.65`

Se analizan métricas como:

* Mejor beneficio
* Media y desviación estándar
* Estabilidad y escalabilidad

## Resultados principales

* Branch and Bound garantiza soluciones óptimas, pero su tiempo de ejecución crece exponencialmente.
* El Recocido Simulado alcanza soluciones óptimas o cercanas al óptimo con menor costo computacional.
* En instancias más complejas, SA presenta variabilidad inherente a su naturaleza estocástica.

##  Ejecución

Cada implementación puede ejecutarse de forma independiente. De manera general:

```bash
python main.py
```

(Revisar cada carpeta para instrucciones específicas).

##  Trabajo futuro

* Evaluar instancias de mayor tamaño.
* Comparar con otras metaheurísticas (algoritmos genéticos, búsqueda tabú).
* Incorporar ajuste automático de parámetros.
* Explorar enfoques emergentes como algoritmos cuánticos para optimización.

##  Referencias

* Balas, E. & Toth, P. *Branch and Bound Methods*, 1983.
* Martello, S. & Toth, P. *Knapsack Problems*, Wiley, 1990.
* Kirkpatrick, S. et al. *Optimization by Simulated Annealing*, Science, 1983.
* Burkardt, J. *KNAPSACK_MULTIPLE Dataset*, Florida State University, 2009.

##  Autores

* **Lucia Francisco Bautista**
* **Luis Eduardo Villanueva Oliver**

Repositorio con fines académicos y de investigación.
