import tkinter as tk
from tkinter import ttk, messagebox
from caotica import busca_em_largura, busca_em_profundidade

class JogoDos8App:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo dos 8")
        self.root.geometry("400x520")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Insira os valores iniciais do tabuleiro:").pack(pady=10)

        self.entries = []
        grid_frame = tk.Frame(self.root)
        grid_frame.pack()
        for i in range(3):
            row = []
            for j in range(3):
                entry = tk.Entry(grid_frame, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                row.append(entry)
            self.entries.append(row)

        tk.Label(self.root, text="Escolha os métodos de resolução:").pack(pady=10)

        self.algoritmos_vars = {
            "Busca em Largura": tk.BooleanVar(),
            "Busca em Profundidade": tk.BooleanVar()
        }

        for nome, var in self.algoritmos_vars.items():
            chk = tk.Checkbutton(self.root, text=nome, variable=var)
            chk.pack(anchor='w', padx=30)

        botao_frame = tk.Frame(self.root)
        botao_frame.pack(pady=20)

        self.btn_resolver = tk.Button(botao_frame, text="Resolver", width=10, command=self.resolver)
        self.btn_resolver.grid(row=0, column=0, padx=10)

        self.btn_sair = tk.Button(botao_frame, text="Sair", width=10, command=self.root.quit)
        self.btn_sair.grid(row=0, column=1, padx=10)

    def resolver(self):
        estado = []
        try:
            for linha in self.entries:
                for entry in linha:
                    texto = entry.get().strip()
                    if texto == "":
                        valor = 0
                    else:
                        valor = int(texto)
                    if not (0 <= valor <= 8):
                        raise ValueError("Os valores devem estar entre 0 e 8.")
                    estado.append(valor)

            # Verifica se contém todos os números de 0 a 8, sem repetições
            if sorted(estado) != list(range(9)):
                raise ValueError("Todos os números de 0 a 8 devem aparecer uma única vez.")
        except Exception as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")
            return

        metodos_selecionados = [nome for nome, var in self.algoritmos_vars.items() if var.get()]

        if not metodos_selecionados:
            messagebox.showwarning("Aviso", "Selecione ao menos um método de resolução.")
            return

        self.resultados = []

        if "Busca em Largura" in metodos_selecionados:
            resultado = busca_em_largura(tuple(estado))
            self.resultados.append(("Busca em Largura", resultado))

        if "Busca em Profundidade" in metodos_selecionados:
            resultado = busca_em_profundidade(tuple(estado))
            self.resultados.append(("Busca em Profundidade", resultado))

        self.resultado_index = 0
        self.mostrar_proximo_resultado()

    def mostrar_proximo_resultado(self):
        if self.resultado_index >= len(self.resultados):
            messagebox.showinfo("Fim", "Todas as resoluções foram exibidas.")
            return

        metodo, resultado = self.resultados[self.resultado_index]
        self.resultado_index += 1
        self.animar_solucao(resultado["solucao"], resultado, metodo)

    
    def animar_solucao(self, solucao, resultado, metodo):
        janela = tk.Toplevel(self.root)
        janela.title(f"Resolução - {metodo}")

        label_metodo = tk.Label(janela, text=f"Método: {metodo}", font=("Arial", 14, "bold"))
        label_metodo.pack(pady=10)

        quadro = tk.Frame(janela)
        quadro.pack()

        labels = [tk.Label(quadro, width=4, height=2, font=("Arial", 16), relief="groove") for _ in range(9)]
        for i, lbl in enumerate(labels):
            lbl.grid(row=i//3, column=i%3, padx=5, pady=5)

        def atualizar_tabuleiro(estado):
            for i, valor in enumerate(estado):
                labels[i].config(text=str(valor) if valor != 0 else "")

        if solucao:
            def animar_passos(i=0):
                if i < len(solucao):
                    atualizar_tabuleiro(solucao[i])
                    janela.after(500, animar_passos, i+1)
                else:
                    mostrar_dados()

            animar_passos()
        else:
            label_erro = tk.Label(janela, text="Solução não encontrada dentro do limite!", fg="red")
            label_erro.pack(pady=10)
            mostrar_dados()

        def mostrar_dados():
            infos = f"""
    Nós gerados: {resultado['nos_gerados']}
    Nós na fronteira: {resultado['nos_fronteira']}
    Profundidade da solução: {resultado['profundidade_solucao']}
    Profundidade máxima: {resultado['profundidade_max']}
    Completo: {resultado['completo']}
    Ótimo: {resultado['otimo']}
    Admissível: {resultado['admissivel']}
            """
            label_result = tk.Label(janela, text=infos.strip(), justify="left")
            label_result.pack(pady=10)

            btn_proximo = tk.Button(janela, text="Próximo", command=lambda: [janela.destroy(), self.mostrar_proximo_resultado()])
            btn_proximo.pack(pady=10)

    def exibir_metrica(self, resultado):
        met_win = tk.Toplevel(self.root)
        met_win.title("Métricas da Solução")
        met_win.geometry("400x300")

        metrics = [
            ("Nós gerados", resultado["nos_gerados"]),
            ("Nós na fronteira", resultado["nos_fronteira"]),
            ("Profundidade da solução", resultado["profundidade_solucao"]),
            ("Profundidade máxima", resultado["profundidade_max"]),
            ("Admissibilidade", resultado["admissivel"]),
            ("Ótima?", "Sim" if resultado["otimo"] else "Não"),
            ("Completa?", "Sim" if resultado["completo"] else "Não")
        ]

        for nome, valor in metrics:
            tk.Label(met_win, text=f"{nome}: {valor}", font=("Arial", 12), anchor="w").pack(fill="x", padx=20, pady=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = JogoDos8App(root)
    root.mainloop()
