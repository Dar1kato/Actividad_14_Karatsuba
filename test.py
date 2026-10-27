"""
Prueba interactiva SIN Karatsuba.

Pide dos números por la terminal, los multiplica directamente con el operador
* de Python y muestra el resultado, el tiempo (ms) y la memoria pico (KB).

La medición se hace igual que en karatsuba.py (promedio de varias corridas
para el tiempo y tracemalloc aparte para la memoria), para que los resultados
sean comparables.

Uso:
    python test.py
"""

import time
import tracemalloc


def leer_entero(mensaje):
    """Pide un entero por terminal. Enter vacío -> None (salir)."""
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            return None
        try:
            return int(texto)
        except ValueError:
            print("  Entrada no válida: escribe un número entero.")


def multiplicar(x, y):
    """Multiplicación directa, sin Karatsuba."""
    return x * y


def medir(x, y, objetivo_s=0.2, maximo=100_000):
    """Devuelve (resultado, tiempo en ms, memoria pico en KB)."""
    # Cuántas repeticiones hacer para que la medición sea estable
    inicio = time.perf_counter()
    multiplicar(x, y)
    una_corrida = max(time.perf_counter() - inicio, 1e-9)
    repeticiones = int(min(maximo, max(1, objetivo_s / una_corrida)))

    # Tiempo: promedio de varias corridas
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        resultado = multiplicar(x, y)
    tiempo_ms = (time.perf_counter() - inicio) / repeticiones * 1000

    # Memoria: pico durante una corrida (aparte, porque tracemalloc ralentiza)
    tracemalloc.start()
    multiplicar(x, y)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return resultado, tiempo_ms, pico / 1024


def main():
    print("Multiplicación directa (sin Karatsuba) — Enter vacío para salir\n")

    while True:
        x = leer_entero("Primer número:  ")
        if x is None:
            break
        y = leer_entero("Segundo número: ")
        if y is None:
            break

        resultado, tiempo_ms, memoria_kb = medir(x, y)

        print(f"\nx * y = {resultado}")
        print(f"Tiempo:  {tiempo_ms:.6f} ms")
        print(f"Memoria: {memoria_kb:.2f} KB\n")


if __name__ == "__main__":
    main()
