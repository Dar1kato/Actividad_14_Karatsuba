# Algoritmo de Karatsuba en Python

Implementación recursiva del algoritmo de Karatsuba para multiplicar enteros grandes, siguiendo el paradigma **Divide y Vencerás**. El script genera números aleatorios de 20, 50 y 100 dígitos, los multiplica y reporta el **tiempo** (ms) y la **memoria** (KB) utilizados.

## Contenido

1. [Requisitos y uso](#requisitos-y-uso)
2. [Descripción del algoritmo](#descripción-del-algoritmo)
3. [Implementación recursiva](#implementación-recursiva)
4. [Medición de tiempo y memoria](#medición-de-tiempo-y-memoria)
5. [Resultados con Karatsuba](#resultados-con-karatsuba)
6. [Comparación: multiplicación sin Karatsuba](#comparación-multiplicación-sin-karatsuba)
7. [Complejidad](#complejidad)

---

## Requisitos y uso

- Python 3.8 o superior.
- No requiere librerías externas (solo módulos de la biblioteca estándar: `random`, `time`, `tracemalloc`).

```bash
python karatsuba.py
```

Para cada tamaño (20, 50 y 100 dígitos) se imprime:

```
--- 20 dígitos ---
x = ...
y = ...
x * y = ...
Tiempo:  ... ms
Memoria: ... KB
```

Los números se generan con una semilla fija (`random.Random(42)`), por lo que las entradas son siempre las mismas y los resultados son reproducibles. Para probar otros números, cambia la semilla en `main()`.

---

## Descripción del algoritmo

La multiplicación escolar de dos números de `N` dígitos requiere `N²` multiplicaciones de un dígito. Karatsuba reduce el costo reemplazando **4 multiplicaciones** de tamaño `N/2` por **3**.

Dados dos números `x` e `y`, y `m = n // 2` (con `n` la cantidad de dígitos del mayor), se parten en una mitad alta y una baja:

```
x = a · 10^m + b
y = c · 10^m + d
```

Entonces:

```
x · y = a·c · 10^(2m) + (a·d + b·c) · 10^m + b·d
```

El término `a·d + b·c` se obtiene sin hacer dos multiplicaciones, usando un solo producto adicional:

```
z2 = a · c
z0 = b · d
z3 = (a + b) · (c + d)
z1 = z3 − z2 − z0        (= a·d + b·c)
```

Y el resultado final es:

```
x · y = z2 · 10^(2m) + z1 · 10^m + z0
```

### Ejemplo: 1234 × 5678

| Paso | Cálculo |
|---|---|
| División | `m = 2` → `a = 12`, `b = 34`, `c = 56`, `d = 78` |
| Conquista | `z2 = 12·56 = 672`, `z0 = 34·78 = 2652`, `z3 = (12+34)·(56+78) = 46·134 = 6164` |
| Integración | `z1 = 6164 − 672 − 2652 = 2840` |
| Resultado | `672·10⁴ + 2840·10² + 2652 = 7 006 652` |

---

## Implementación recursiva

El script separa el algoritmo en las tres fases del paradigma Divide y Vencerás, cada una en su propia función:

| Fase | Función | Qué hace |
|---|---|---|
| **División** | `dividir(x, y)` | Calcula `m` y parte `x` e `y` en `(a, b)` y `(c, d)` con `divmod(·, 10**m)`. |
| **Conquista** | `conquistar(a, b, c, d)` | Resuelve los 3 subproblemas llamando recursivamente a `karatsuba()`: `a·c`, `b·d` y `(a+b)·(c+d)`. |
| **Integración** | `integrar(z0, z3, z2, m)` | Calcula `z1 = z3 − z2 − z0` y combina `z2·10^(2m) + z1·10^m + z0`. |

La función principal une las tres fases:

```python
def karatsuba(x, y):
    # Caso base: algún operando de 1 dígito
    if x < 10 or y < 10:
        return x * y

    a, b, c, d, m = dividir(x, y)           # 1. División
    z0, z3, z2 = conquistar(a, b, c, d)     # 2. Conquista
    return integrar(z0, z3, z2, m)          # 3. Integración
```

### Recursión

- **Caso base:** si alguno de los dos operandos tiene un solo dígito (`< 10`), se multiplica directamente.
- **Caso recursivo:** el problema se divide en 3 subproblemas de aproximadamente la mitad de tamaño. Cada subproblema vuelve a pasar por `karatsuba()`, que aplica de nuevo las tres fases.
- **Subproblema `(a+b)·(c+d)`:** la suma puede tener un dígito más que cada mitad, por lo que este subproblema puede ser ligeramente mayor que `N/2`. El algoritmo termina igualmente, porque los valores siguen disminuyendo en cada nivel.
- **Profundidad de recursión:** crece aproximadamente como `log₂(N)`, por lo que no hay riesgo de alcanzar el límite de recursión de Python con estos tamaños.

> Nota: la multiplicación por potencias de 10 (`10**m`, `10**(2*m)`) equivale a un desplazamiento de dígitos en base 10; no cuenta como una multiplicación "real" del algoritmo.

---

## Medición de tiempo y memoria

Ambas mediciones están en la función `medir(x, y, repeticiones=100)`, que devuelve `(resultado, tiempo_ms, memoria_kb)`.

### Tiempo

Se usa `time.perf_counter()` (reloj de alta resolución). Como una sola multiplicación tarda menos de un par de milisegundos, y una sola medición sería muy ruidosa, se ejecuta `karatsuba(x, y)` **100 veces** y se reporta el **promedio**:

```python
inicio = time.perf_counter()
for _ in range(repeticiones):
    resultado = karatsuba(x, y)
tiempo_ms = (time.perf_counter() - inicio) / repeticiones * 1000
```

### Memoria

Se usa el módulo `tracemalloc`, que registra las asignaciones de memoria de Python. Se reporta el **pico** de memoria durante una corrida:

```python
tracemalloc.start()
karatsuba(x, y)
_, pico = tracemalloc.get_traced_memory()
tracemalloc.stop()
memoria_kb = pico / 1024
```

Consideraciones:

- La memoria se mide en una **corrida aparte** del tiempo, porque `tracemalloc` ralentiza la ejecución y distorsionaría el tiempo.
- `tracemalloc` solo cuenta memoria asignada por Python durante la ejecución; no incluye el intérprete ni los números `x` e `y` creados antes de iniciar la medición.
- Los tiempos dependen de la computadora, del sistema operativo y de la carga en ese momento. Es normal que varíen entre ejecuciones y entre equipos.

---

## Resultados con Karatsuba

Resultados obtenidos con la semilla `42` (los tiempos pueden variar en otra máquina):

| Dígitos | Tiempo (ms) | Memoria (KB) |
|---|---|---|
| 20 | 0.157 | 0.88 |
| 50 | 0.678 | 1.32 |
| 100 | 1.607 | 1.75 |

---

## Comparación: multiplicación sin Karatsuba

> Sección para completar. Aquí se registrará el tiempo que tarda cada multiplicación **sin** utilizar el algoritmo de Karatsuba, usando los mismos números (semilla `42`) para que la comparación sea justa.

| Dígitos | Tiempo sin Karatsuba (ms) | Memoria sin Karatsuba (KB) | Tiempo con Karatsuba (ms) | Memoria con Karatsuba (KB) |
|---|---|---|---|---|
| 20 | _pendiente_ | _pendiente_ | 0.157 | 0.88 |
| 50 | _pendiente_ | _pendiente_ | 0.678 | 1.32 |
| 100 | _pendiente_ | _pendiente_ | 1.607 | 1.75 |

**Método utilizado:** _pendiente_

**Observaciones:** _pendiente_

---

## Complejidad

### Tiempo

La recurrencia de Karatsuba es:

```
T(N) = 3 · T(N/2) + O(N)
```

Por el teorema maestro:

```
T(N) ∈ Θ(N^log₂(3)) ≈ Θ(N^1.585)
```

Frente a `Θ(N²)` de la multiplicación escolar.

| Término | Origen |
|---|---|
| `3 · T(N/2)` | Los 3 subproblemas de la fase de **conquista**. |
| `O(N)` | Las sumas, restas y desplazamientos de las fases de **división** e **integración**. |

### Espacio

- La profundidad de la pila de recursión es `O(log N)`.
- Cada nivel retiene operandos de la mitad de tamaño que el anterior (`N + N/2 + N/4 + …`), por lo que el espacio total es:

```
S(N) ∈ Θ(N)
```
