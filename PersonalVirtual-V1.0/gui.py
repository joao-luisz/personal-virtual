# gui.py

import tkinter as tk
from tkinter import messagebox
from modules.chatbot import iniciar_chatbot
from modules.user_management import (
    cadastrar_usuario,
    verificar_login,
    salvar_progresso,
    recuperar_historico_progresso,
    exibir_meus_treinos,
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PersonalTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Trainer Virtual")
        self.root.geometry("800x600")

        # ID do usuário (será definido após o login)
        self.usuario_id = None

        # Tela inicial: Login ou Cadastro
        self.tela_inicial()

    def limpar_tela(self):
        """Limpa todos os widgets da tela."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def tela_inicial(self):
        """Exibe a tela inicial com opções de Login e Cadastro."""
        self.limpar_tela()

        # Título
        titulo = tk.Label(self.root, text="=== BEM-VINDO AO PERSONAL TRAINER VIRTUAL ===", font=("Arial", 16))
        titulo.pack(pady=20)

        # Botões para login e cadastro
        tk.Button(self.root, text="Login", command=self.tela_login, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Cadastrar", command=self.tela_cadastro, width=30, height=2).pack(pady=10)

    def tela_login(self):
        """Exibe a tela de login."""
        self.limpar_tela()

        # Título
        titulo = tk.Label(self.root, text="LOGIN", font=("Arial", 14))
        titulo.pack(pady=20)

        # Campos de entrada
        tk.Label(self.root, text="Nome de Usuário:").pack()
        nome_usuario_var = tk.StringVar()
        tk.Entry(self.root, textvariable=nome_usuario_var).pack()

        tk.Label(self.root, text="Senha:").pack()
        senha_var = tk.StringVar()
        tk.Entry(self.root, textvariable=senha_var, show="*").pack()

        # Botão para fazer login
        tk.Button(
            self.root,
            text="Entrar",
            command=lambda: self.fazer_login(nome_usuario_var.get(), senha_var.get()),
        ).pack(pady=20)

        # Botão para voltar à tela inicial
        tk.Button(self.root, text="Voltar", command=self.tela_inicial).pack()

    def fazer_login(self, nome_usuario, senha):
        """Verifica o login no backend."""
        usuario_id = verificar_login(nome_usuario, senha)
        if usuario_id:
            self.usuario_id = usuario_id
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.criar_menu()
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos.")

    def tela_cadastro(self):
        """Exibe a tela de cadastro."""
        self.limpar_tela()

        # Título
        titulo = tk.Label(self.root, text="CADASTRO", font=("Arial", 14))
        titulo.pack(pady=20)

        # Campos de entrada
        campos = [
            ("Nome de Usuário:", tk.StringVar()),
            ("E-mail ou Telefone:", tk.StringVar()),
            ("Senha:", tk.StringVar()),
            ("Nome Preferido:", tk.StringVar()),
            ("Idade:", tk.IntVar(value=18)),
            ("Peso (kg):", tk.DoubleVar(value=70.0)),
            ("Altura (cm):", tk.DoubleVar(value=170.0)),
            ("Nível de Experiência:", tk.StringVar(value="Iniciante")),
            ("Objetivo:", tk.StringVar(value="Emagrecimento")),
        ]

        entradas = {}
        for texto, variavel in campos:
            tk.Label(self.root, text=texto).pack()
            entrada = tk.Entry(self.root, textvariable=variavel)
            entrada.pack()
            entradas[texto] = variavel

        # Botão para cadastrar
        tk.Button(
            self.root,
            text="Cadastrar",
            command=lambda: self.cadastrar_usuario_gui(
                entradas["Nome de Usuário:"].get(),
                entradas["E-mail ou Telefone:"].get(),
                entradas["Senha:"].get(),
                entradas["Nome Preferido:"].get(),
                entradas["Idade:"].get(),
                entradas["Peso (kg):"].get(),
                entradas["Altura (cm):"].get(),
                entradas["Nível de Experiência:"].get(),
                entradas["Objetivo:"].get(),
            ),
        ).pack(pady=20)

        # Botão para voltar à tela inicial
        tk.Button(self.root, text="Voltar", command=self.tela_inicial).pack()

    def cadastrar_usuario_gui(self, nome_usuario, email_ou_telefone, senha, nome_preferido, idade, peso, altura, nivel_experiencia, objetivo):
        """Chama o backend para cadastrar o usuário."""
        try:
            cadastrar_usuario(nome_usuario, email_ou_telefone, senha, nome_preferido, idade, peso, altura, nivel_experiencia, objetivo)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.tela_inicial()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def criar_menu(self):
        """Exibe o menu principal após o login."""
        self.limpar_tela()

        # Título
        titulo = tk.Label(self.root, text="MENU PRINCIPAL", font=("Arial", 14))
        titulo.pack(pady=20)

        # Botões do menu
        botoes = [
            ("Gerar Planilha de Treino", self.gerar_planilha),
            ("Registrar Progresso", self.registrar_progresso),
            ("Ver Histórico de Progresso", self.ver_historico_progresso),
            ("Exibir Meus Treinos Salvos", self.exibir_meus_treinos),
            ("Sair", self.sair),
        ]

        for texto, comando in botoes:
            botao = tk.Button(self.root, text=texto, command=comando, width=30, height=2)
            botao.pack(pady=10)

    def gerar_planilha(self):
        """Exibe a tela para gerar uma planilha de treino."""
        self.limpar_tela()

        # Título
        titulo = tk.Label(self.root, text="GERAR PLANILHA DE TREINO", font=("Arial", 14))
        titulo.pack(pady=20)

        # Campos de entrada
        tk.Label(self.root, text="Gênero:").pack()
        genero_var = tk.StringVar(value="Masculino")
        tk.Radiobutton(self.root, text="Masculino", variable=genero_var, value="Masculino").pack()
        tk.Radiobutton(self.root, text="Feminino", variable=genero_var, value="Feminino").pack()

        tk.Label(self.root, text="Dias disponíveis para treinar:").pack()
        dias_var = tk.IntVar(value=3)
        tk.Entry(self.root, textvariable=dias_var).pack()

        tk.Label(self.root, text="Acesso a equipamentos de academia?").pack()
        equipamentos_var = tk.StringVar(value="Sim")
        tk.Radiobutton(self.root, text="Sim", variable=equipamentos_var, value="Sim").pack()
        tk.Radiobutton(self.root, text="Não", variable=equipamentos_var, value="Não").pack()

        # Botão para gerar a planilha
        tk.Button(
            self.root,
            text="Gerar Planilha",
            command=lambda: self.exibir_planilha(genero_var.get(), dias_var.get(), equipamentos_var.get()),
        ).pack(pady=20)

        # Botão para voltar ao menu
        tk.Button(self.root, text="Voltar ao Menu", command=self.criar_menu).pack()

    def exibir_planilha(self, genero, dias_disponiveis, equipamentos):
        """Exibe a planilha de treino gerada."""
        try:
            planilha_traduzida = iniciar_chatbot(self.usuario_id, genero, dias_disponiveis, equipamentos)

            self.limpar_tela()

            # Título
            titulo = tk.Label(self.root, text="PLANILHA DE TREINO RECOMENDADA", font=("Arial", 14))
            titulo.pack(pady=20)

            # Exibir a planilha
            for dia, info in planilha_traduzida.items():
                grupo_muscular = info["grupo_muscular"]
                exercicios = info["exercicios"]

                frame_dia = tk.Frame(self.root)
                frame_dia.pack(pady=10)

                tk.Label(frame_dia, text=f"=== {dia}: {grupo_muscular} ===", font=("Arial", 12)).pack()
                for i, exercicio in enumerate(exercicios, 1):
                    tk.Label(frame_dia, text=f"{i}. {exercicio}").pack()

            # Botão para voltar ao menu
            tk.Button(self.root, text="Voltar ao Menu", command=self.criar_menu).pack(pady=20)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar a planilha: {e}")

    def registrar_progresso(self):
        """Exibe a tela para registrar progresso."""
        self.limpar_tela()

        # Título
        titulo = tk.Label(self.root, text="REGISTRAR PROGRESSO", font=("Arial", 14))
        titulo.pack(pady=20)

        # Campos de entrada
        tk.Label(self.root, text="Peso atual (kg):").pack()
        peso_var = tk.DoubleVar()
        tk.Entry(self.root, textvariable=peso_var).pack()

        tk.Label(self.root, text="Medidas corporais (separadas por vírgulas):").pack()
        medidas_var = tk.StringVar()
        tk.Entry(self.root, textvariable=medidas_var).pack()

        tk.Label(self.root, text="Observações adicionais:").pack()
        observacoes_var = tk.StringVar()
        tk.Entry(self.root, textvariable=observacoes_var).pack()

        # Botão para salvar o progresso
        tk.Button(
            self.root,
            text="Salvar Progresso",
            command=lambda: self.salvar_progresso_gui(peso_var.get(), medidas_var.get(), observacoes_var.get()),
        ).pack(pady=20)

        # Botão para voltar ao menu
        tk.Button(self.root, text="Voltar ao Menu", command=self.criar_menu).pack()

    def salvar_progresso_gui(self, peso, medidas, observacoes):
        """Salva o progresso do usuário."""
        salvar_progresso(self.usuario_id, peso, medidas.split(","), observacoes)
        messagebox.showinfo("Sucesso", "Progresso registrado com sucesso!")
        self.criar_menu()

    def ver_historico_progresso(self):
        """Exibe o histórico de progresso do usuário."""
        self.limpar_tela()

        # Título
        titulo = tk.Label(self.root, text="HISTÓRICO DE PROGRESSO", font=("Arial", 14))
        titulo.pack(pady=20)

        # Recuperar o histórico
        historico = recuperar_historico_progresso(self.usuario_id)
        if not historico:
            tk.Label(self.root, text="Você ainda não registrou nenhum progresso.").pack()
            tk.Button(self.root, text="Voltar ao Menu", command=self.criar_menu).pack()
            return

        # Exibir o histórico
        for registro in historico:
            frame_registro = tk.Frame(self.root)
            frame_registro.pack(pady=5)

            tk.Label(frame_registro, text=f"Data: {registro['data']}").pack()
            tk.Label(frame_registro, text=f"Peso: {registro['peso']} kg").pack()
            if registro['medidas']:
                tk.Label(frame_registro, text=f"Medidas: {', '.join(registro['medidas'])}").pack()
            if registro['observacoes']:
                tk.Label(frame_registro, text=f"Observações: {registro['observacoes']}").pack()

        # Gerar gráfico de progresso
        datas = [registro['data'] for registro in historico]
        pesos = [registro['peso'] for registro in historico]

        figura = plt.Figure(figsize=(6, 4), dpi=100)
        ax = figura.add_subplot(111)
        ax.plot(datas, pesos, marker='o')
        ax.set_title("Progresso de Peso ao Longo do Tempo")
        ax.set_xlabel("Data")
        ax.set_ylabel("Peso (kg)")
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(figura, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Botão para voltar ao menu
        tk.Button(self.root, text="Voltar ao Menu", command=self.criar_menu).pack(pady=20)

    def exibir_meus_treinos(self):
        """Exibe os treinos salvos pelo usuário."""
        self.limpar_tela()

        # Título
        titulo = tk.Label(self.root, text="MEUS TREINOS SALVOS", font=("Arial", 14))
        titulo.pack(pady=20)

        # Recuperar os treinos salvos
        treinos = exibir_meus_treinos(self.usuario_id)

        if not treinos:
            tk.Label(self.root, text="Você ainda não possui nenhum treino salvo.").pack()
            tk.Button(self.root, text="Voltar ao Menu", command=self.criar_menu).pack()
            return

        # Exibir os treinos
        for data, exercicios in treinos:
            frame_treino = tk.Frame(self.root)
            frame_treino.pack(pady=5)

            tk.Label(frame_treino, text=f"Treino - Data: {data}").pack()
            for i, exercicio in enumerate(exercicios.split(", "), 1):
                tk.Label(frame_treino, text=f"{i}. {exercicio}").pack()

        # Botão para voltar ao menu
        tk.Button(self.root, text="Voltar ao Menu", command=self.criar_menu).pack(pady=20)

    def sair(self):
        """Encerra o programa."""
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalTrainerApp(root)
    root.mainloop()