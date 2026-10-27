"""
Algoritmo de Karatsuba — Divide y Vencerás

Multiplica dos enteros de N dígitos en O(N^log2(3)).
Fases:
    1. dividir()    -> DIVISIÓN
    2. conquistar() -> CONQUISTA
    3. integrar()   -> INTEGRACIÓN DE LA SOLUCIÓN

Uso:
    python karatsuba.py
"""

import random
import time
import tracemalloc


# ----------------------------------------------------------------------------
# FASE 1 — DIVISIÓN
# ----------------------------------------------------------------------------
def dividir(x, y):
    """Parte x = a·10^m + b  y  y = c·10^m + d. Devuelve (a, b, c, d, m)."""
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    base = 10 ** m
    a, b = divmod(x, base)
    c, d = divmod(y, base)
    return a, b, c, d, m


# ----------------------------------------------------------------------------
# FASE 2 — CONQUISTA
# ----------------------------------------------------------------------------
def conquistar(a, b, c, d):
    """Resuelve los 3 subproblemas recursivamente: a·c, b·d y (a+b)(c+d)."""
    z2 = karatsuba(a, c)
    z0 = karatsuba(b, d)
    z3 = karatsuba(a + b, c + d)
    return z0, z3, z2


# ----------------------------------------------------------------------------
# FASE 3 — INTEGRACIÓN DE LA SOLUCIÓN
# ----------------------------------------------------------------------------
def integrar(z0, z3, z2, m):
    """z1 = z3 − z2 − z0  y  x·y = z2·10^2m + z1·10^m + z0."""
    z1 = z3 - z2 - z0
    return z2 * 10 ** (2 * m) + z1 * 10 ** m + z0


# ----------------------------------------------------------------------------
# Karatsuba
# ----------------------------------------------------------------------------
def karatsuba(x, y):
    # Caso base: algún operando de 1 dígito
    if x < 10 or y < 10:
        return x * y

    a, b, c, d, m = dividir(x, y)           # 1. División
    z0, z3, z2 = conquistar(a, b, c, d)     # 2. Conquista
    return integrar(z0, z3, z2, m)          # 3. Integración


# ----------------------------------------------------------------------------
# Mediciones
# ----------------------------------------------------------------------------
def medir(x, y, repeticiones=100):
    """Devuelve (resultado, tiempo en ms, memoria pico en KB)."""
    # Tiempo: promedio de varias corridas (tracemalloc se usa aparte porque
    # distorsiona el tiempo)
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        resultado = karatsuba(x, y)
    tiempo_ms = (time.perf_counter() - inicio) / repeticiones * 1000

    # Memoria: pico durante una corrida
    tracemalloc.start()
    karatsuba(x, y)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return resultado, tiempo_ms, pico / 1024


def numero_aleatorio(n_digitos, rng):
    """Entero con exactamente n_digitos dígitos."""
    return rng.randint(10 ** (n_digitos - 1), 10 ** n_digitos - 1)


def main():
    rng = random.Random(42)  # semilla fija -> resultados reproducibles

    for n in (20, 50, 100):
        x = numero_aleatorio(n, rng)
        y = numero_aleatorio(n, rng)
        resultado, tiempo_ms, memoria_kb = medir(x, y)

        print(f"--- {n} dígitos ---")
        print(f"x = {x}")
        print(f"y = {y}")
        print(f"x * y = {resultado}")
        print(f"Tiempo:  {tiempo_ms:.3f} ms")
        print(f"Memoria: {memoria_kb:.2f} KB")
        print()


if __name__ == "__main__":
    main()
