import tkinter as tk
from tkinter import ttk, messagebox
from tabulate import tabulate
import numpy as np


# Clase para el algoritmo FIFO (First In First Out)
class AlgoritmoFIFO:
    def __init__(self, marcos):
        self.marcos = marcos

    def ejecutar(self, paginas):
        marcos = ["-"] * self.marcos
        puntero = 0
        fallos = []
        estado = []

        for pagina in paginas:
            if pagina not in marcos:
                marcos[puntero] = pagina
                puntero = (puntero + 1) % self.marcos
                fallos.append("F")
            else:
                fallos.append("/")
            estado.append(marcos[:])
        return estado, fallos


# Clase para el algoritmo LRU (Least Recently Used)
class AlgoritmoLRU:
    def __init__(self, marcos):
        self.marcos = marcos

    def ejecutar(self, paginas):
        marcos = []
        fallos = []
        estado = []

        for pagina in paginas:
            if pagina not in marcos:
                if len(marcos) < self.marcos:
                    marcos.append(pagina)
                else:
                    marcos.pop(0)
                    marcos.append(pagina)
                fallos.append("F")
            else:
                marcos.remove(pagina)
                marcos.append(pagina)
                fallos.append("/")
            estado.append(marcos[:] + ["-"] * (self.marcos - len(marcos)))
        return estado, fallos


# Clase para el algoritmo Óptimo (solo para medición interna)
class AlgoritmoOptimo:
    def __init__(self, marcos):
        self.marcos = marcos

    def ejecutar(self, paginas):
        marcos = []
        fallos = []

        for i in range(len(paginas)):
            pagina = paginas[i]
            if pagina not in marcos:
                if len(marcos) < self.marcos:
                    marcos.append(pagina)
                else:
                    futuro = paginas[i + 1:]
                    indices = [futuro.index(p) if p in futuro else float("inf") for p in marcos]
                    reemplazo = indices.index(max(indices))
                    marcos[reemplazo] = pagina
                fallos.append("F")
            else:
                fallos.append("/")
        total_fallos_optimo = fallos.count("F")
        return total_fallos_optimo  # Solo devolvemos los fallos


# Función para ejecutar los algoritmos y mostrar resultados
def ejecutar_algoritmos():
    entrada = entrada_paginas.get()
    try:
        paginas = [int(p.strip()) for p in entrada.split(",")]
    except:
        messagebox.showerror("Error", "Entrada inválida")
        return
    try:
        marcos = int(entry_marcos.get())
        if marcos <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Número de marcos inválido")
        return

    resultados = ""
    algoritmos = [
        ("FIFO", AlgoritmoFIFO(marcos)),
        ("LRU", AlgoritmoLRU(marcos)),
    ]

    # Instanciamos el algoritmo Óptimo solo para medición
    algoritmo_optimo = AlgoritmoOptimo(marcos)
    fallos_optimo = algoritmo_optimo.ejecutar(paginas)

    for nombre, algoritmo in algoritmos:
        estado, fallos = algoritmo.ejecutar(paginas)
        total_fallos = fallos.count("F")
        eficiencia = ((len(paginas) - total_fallos) / len(paginas)) * 100

        transpuesta = np.array(estado).T.tolist()
        resultados += f"\n\nAlgoritmo: {nombre}\n"
        resultados += "  " + "  ".join(map(str, paginas)) + "\n"
        resultados += tabulate(transpuesta, tablefmt="fancy_grid") + "\n"
        resultados += "  " + "  ".join(fallos) + "\n"

        resultados += f"Fallos de página: {total_fallos}\n"
        resultados += f"Eficiencia: {eficiencia:.2f}%\n"

    # Mostrar los resultados solo de FIFO y LRU
    text_resultado.config(state=tk.NORMAL)
    text_resultado.delete("1.0", tk.END)
    text_resultado.insert(tk.END, resultados)
    text_resultado.config(state=tk.DISABLED)

    # Mostrar las estadísticas en la interfaz
    label_fallos.config(text=f"Fallos Totales (Óptimo): {fallos_optimo}")
    label_eficiencia.config(text=f"Eficiencia (FIFO y LRU): {eficiencia:.2f}%")


# Ventana principal de la aplicación
root = tk.Tk()
root.title("Gestor de Memoria Virtual Simplificado")

frame = ttk.Frame(root, padding="10")
frame.pack(fill="both", expand=True)

# Etiquetas y campos de entrada
ttk.Label(frame, text="Cadena de páginas (ej: 0,1,2,3,0,1,4):").pack(pady=5)
entrada_paginas = ttk.Entry(frame, width=50)
entrada_paginas.pack()

ttk.Label(frame, text="Número de marcos:").pack(pady=5)
entry_marcos = ttk.Entry(frame)
entry_marcos.pack()

# Botón para ejecutar la simulación
ttk.Button(frame, text="Ejecutar Simulación", command=ejecutar_algoritmos).pack(pady=10)

# Cuadro de texto para resultados
text_resultado = tk.Text(frame, wrap="word", height=15, width=80)
text_resultado.pack(fill="both", expand=True)
text_resultado.config(state=tk.DISABLED, font=("Courier", 10))

# Etiquetas para mostrar las estadísticas
label_fallos = ttk.Label(frame, text="Fallos Totales: 0")
label_fallos.pack(pady=5)

label_eficiencia = ttk.Label(frame, text="Eficiencia: 0.00%")
label_eficiencia.pack(pady=5)

# Iniciar la aplicación
root.mainloop()
