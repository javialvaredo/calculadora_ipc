import tkinter as tk
from tkinter import messagebox

class IPC:
    def calcular_periodo(self, meses):
        acumulado = 1
        for valor in meses.values():
            acumulado *= (1 + valor / 100)
        acumulado -= 1
        return round(acumulado * 100, 2)

    def imprimir_ipc_mensual(self, meses):
        acumulado = 1
        resultados = []
        for i, (mes, valor) in enumerate(meses.items()):
            if i == 0:
                acumulado *= (1 + valor / 100)
                resultados.append(f"{mes.capitalize()}: {round(valor, 2)}%")
            else:
                acumulado *= (1 + valor / 100)
                ipc_acumulado = (acumulado - 1) * 100
                resultados.append(f"{mes.capitalize()}: {round(ipc_acumulado, 2)}%")
        return resultados


class VentanaIPC:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de IPC")
        self.meses = {}
        self.ipc = IPC()
        self.resultado_mostrado = False  # <- NUEVA VARIABLE

        # Entradas
        tk.Label(root, text="Mes:").grid(row=0, column=0)
        self.entry_mes = tk.Entry(root)
        self.entry_mes.grid(row=0, column=1)

        tk.Label(root, text="IPC (%):").grid(row=1, column=0)
        self.entry_valor = tk.Entry(root)
        self.entry_valor.grid(row=1, column=1)

        # Botones
        tk.Button(root, text="Agregar", command=self.agregar_mes).grid(row=2, column=0, pady=5)
        tk.Button(root, text="Calcular", command=self.calcular).grid(row=2, column=1, pady=5)

        # Lista y resultados
        tk.Label(root, text="Meses ingresados:").grid(row=3, column=0, columnspan=2)
        self.listbox = tk.Listbox(root, width=40)
        self.listbox.grid(row=4, column=0, columnspan=2, pady=5)

        self.resultado = tk.Text(root, width=40, height=10, state="disabled")
        self.resultado.grid(row=5, column=0, columnspan=2, pady=10)

        # Enter = Agregar
        self.root.bind('<Return>', lambda event: self.agregar_mes())

    def agregar_mes(self):
        # Si ya se calculó, reiniciar todo
        if self.resultado_mostrado:
            self.reiniciar()

        mes = self.entry_mes.get().strip().lower()
        try:
            valor = float(self.entry_valor.get().strip())
            if mes:
                self.meses[mes] = valor
                self.actualizar_lista()
                self.entry_mes.delete(0, tk.END)
                self.entry_valor.delete(0, tk.END)
                self.entry_mes.focus()
            else:
                messagebox.showwarning("Error", "El nombre del mes no puede estar vacío.")
        except ValueError:
            messagebox.showerror("Error", "Ingresá un número válido para el IPC.")

    def calcular(self):
        if not self.meses:
            messagebox.showwarning("Sin datos", "Agregá al menos un mes.")
            return

        total = self.ipc.calcular_periodo(self.meses)
        detalles = self.ipc.imprimir_ipc_mensual(self.meses)

        self.listbox.grid_remove()
        self.resultado.configure(state="normal")
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, f"IPC total: {total}%\n\n")
        for linea in detalles:
            self.resultado.insert(tk.END, linea + "\n")
        self.resultado.configure(state="disabled")

        self.resultado_mostrado = True  # <- Marcar que se calculó

    def reiniciar(self):
        # Limpiar todo
        self.meses = {}
        self.resultado_mostrado = False
        self.resultado.configure(state="normal")
        self.resultado.delete(1.0, tk.END)
        self.resultado.configure(state="disabled")
        self.listbox.delete(0, tk.END)
        self.listbox.grid()  # volver a mostrar el listbox

    def actualizar_lista(self):
        self.listbox.delete(0, tk.END)
        for mes, valor in self.meses.items():
            self.listbox.insert(tk.END, f"{mes.capitalize()}: {valor}%")



def main():
    root = tk.Tk()
    app = VentanaIPC(root)
    root.mainloop()


if __name__ == "__main__":
    main()
