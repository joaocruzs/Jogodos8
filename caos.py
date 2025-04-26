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
        # Parâmetros da animação
        TILE_SIZE  = 100
        ANIM_STEPS = 10
        ANIM_DELAY = 30  # ms entre passos

        janela = tk.Toplevel(self.root)
        janela.title(f"Resolução - {metodo}")

        label_metodo = tk.Label(janela, text=f"Método: {metodo}", font=("Arial", 14, "bold"))
        label_metodo.pack(pady=10)

        canvas = tk.Canvas(janela, width=3*TILE_SIZE, height=3*TILE_SIZE, bg='white')
        canvas.pack()

        # Cria uma lista de posições para cada estado da solução
        positions = []
        for state in solucao:
            pos = {val: (i // 3, i % 3) for i, val in enumerate(state)}
            positions.append(pos)

        # Cria os "tiles" para cada peça
        tiles = {}
        for num in range(9):
            cor = 'lightgray' if num == 0 else 'lightblue'
            rect = canvas.create_rectangle(0, 0, 0, 0, fill=cor, outline='black')
            txt = canvas.create_text(0, 0, text=("" if num == 0 else str(num)), font=('Arial', 24))
            tiles[num] = (rect, txt)

        def update_tiles(pos):
            for num, (i, j) in pos.items():
                x0 = j * TILE_SIZE
                y0 = i * TILE_SIZE
                x1 = x0 + TILE_SIZE
                y1 = y0 + TILE_SIZE
                rect, txt = tiles[num]
                canvas.coords(rect, x0, y0, x1, y1)
                canvas.coords(txt, x0 + TILE_SIZE//2, y0 + TILE_SIZE//2)

        update_tiles(positions[0])
        janela.update()  # Força o redraw inicial
        self.step = 0

        def animate_step():
            if self.step + 1 >= len(positions):
                # Exibe as métricas no fim da animação
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
                return

            cur = positions[self.step]
            nxt = positions[self.step + 1]

            # Identifica a posição vazia no estado atual (chave 0)
            zi, zj = cur[0]

            # Encontra a peça que moverá para a posição do 0
            moving = next(num for num, (ni, nj) in nxt.items() if num != 0 and (ni, nj) == (zi, zj))
            si, sj = cur[moving]     # posição atual da peça
            ti, tj = cur[0]          # destino: onde estava o 0 no estado atual

            dx = (tj - sj) * TILE_SIZE / ANIM_STEPS
            dy = (ti - si) * TILE_SIZE / ANIM_STEPS

            def slide(count=0):
                rect, txt = tiles[moving]
                canvas.move(rect, dx, dy)
                canvas.move(txt, dx, dy)
                if count + 1 < ANIM_STEPS:
                    janela.after(ANIM_DELAY, slide, count + 1)
                else:
                    # Não chamamos update_tiles aqui para não resetar a animação
                    self.step += 1
                    janela.after(200, animate_step)

            slide()

        janela.after(500, animate_step)

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
