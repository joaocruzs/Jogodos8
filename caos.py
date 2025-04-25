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

        cell_size = 120
        canvas = tk.Canvas(janela, width=3*cell_size, height=3*cell_size)
        canvas.pack()

        # Desenha o estado inicial
        items = {}  # Mapear valor da peça para (id do retângulo, id do texto)
        estado_inicial = solucao[0] if solucao else resultado.get("estado_inicial", tuple(range(9)))
        for i, v in enumerate(estado_inicial):
            if v == 0:
                continue
            r, c = divmod(i, 3)
            x, y = c * cell_size, r * cell_size
            rect = canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill="lightblue", outline="black")
            txt = canvas.create_text(x + cell_size/2, y + cell_size/2, text=str(v), font=("Arial", 24))
            items[v] = (rect, txt)

        def mover(v, dr, dc, passo=0, callback=None):
            # Incrementa a animação em 10 passos
            if passo < 10:
                dx = (dc * cell_size) / 10
                dy = (dr * cell_size) / 10
                rect, txt = items[v]
                canvas.move(rect, dx, dy)
                canvas.move(txt, dx, dy)
                janela.after(50, mover, v, dr, dc, passo + 1, callback)
            else:
                if callback:
                    callback()

        def avancar(i=0):
            if i >= len(solucao) - 1:
                mostrar_dados()
                return

            estado_atual = solucao[i]
            estado_prox = solucao[i + 1]
            # Detecta a peça que se moveu: onde o valor na próxima configuração foi substituído pelo zero
            for pos, (atual, prox) in enumerate(zip(estado_atual, estado_prox)):
                if atual != prox and estado_prox[pos] == 0:
                    peca = atual
                    break

            pos_antiga = estado_atual.index(peca)
            pos_nova = estado_prox.index(peca)
            dr = (pos_nova // 3) - (pos_antiga // 3)
            dc = (pos_nova % 3) - (pos_antiga % 3)
            mover(peca, dr, dc, 0, lambda: avancar(i + 1))

        def mostrar_dados():
            infos = (
                f"Nós gerados: {resultado['nos_gerados']}\n"
                f"Nós na fronteira: {resultado['nos_fronteira']}\n"
                f"Profundidade da solução: {resultado['profundidade_solucao']}\n"
                f"Profundidade máxima: {resultado['profundidade_max']}\n"
                f"Completo: {resultado['completo']}\n"
                f"Ótimo: {resultado['otimo']}\n"
                f"Admissível: {resultado['admissivel']}"
            )
            tk.Label(janela, text=infos, justify="left").pack(pady=10)
            tk.Button(janela, text="Próximo", command=lambda: [janela.destroy(), self.mostrar_proximo_resultado()]).pack(pady=10)

        if solucao:
            avancar(0)
        else:
            tk.Label(janela, text="Solução não encontrada!", fg="red").pack(pady=10)
            mostrar_dados()

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
