# app.py

from modules.chatbot import iniciar_chatbot
from modules.user_management import (
    criar_banco_dados,
    cadastrar_usuario,
    verificar_login,
    salvar_progresso,
    recuperar_historico_progresso,
    exibir_meus_treinos
)
from modules.health_metrics import exibir_metricas_saude  # Importar função para exibir métricas de saúde


def tela_inicial():
    """Exibe a tela inicial com opções de Login e Cadastro."""
    print("\n=== BEM-VINDO AO PERSONAL TRAINER VIRTUAL ===")
    print("1. Login")
    print("2. Cadastrar")
    print("3. Sair")
    escolha = input("Escolha uma opção: ")
    return escolha


def tela_login():
    """Exibe a tela de login."""
    print("\n=== LOGIN ===")
    nome_usuario = input("Nome de Usuário: ")
    senha = input("Senha: ")
    usuario_id = verificar_login(nome_usuario, senha)
    if usuario_id:
        print("Login realizado com sucesso!")
        return usuario_id
    else:
        print("Erro: Nome de usuário ou senha incorretos.")
        return None


def tela_cadastro():
    """Exibe a tela de cadastro."""
    print("\n=== CADASTRO ===")
    nome_usuario = input("Nome de Usuário: ")
    email_ou_telefone = input("E-mail ou Telefone: ")
    senha = input("Senha: ")
    nome_preferido = input("Nome Preferido: ")
    idade = int(input("Idade: "))
    peso = float(input("Peso (kg): "))
    altura = float(input("Altura (cm): "))
    nivel_experiencia = input("Nível de Experiência (Iniciante/Intermediário/Avançado): ")
    objetivo = input("Objetivo (Emagrecimento/Hipertrofia/Condicionamento): ")
    try:
        cadastrar_usuario(nome_usuario, email_ou_telefone, senha, nome_preferido, idade, peso, altura, nivel_experiencia, objetivo)
        print("Usuário cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")


def menu_principal(usuario_id):
    """Exibe o menu principal após o login."""
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Gerar Planilha de Treino")
        print("2. Registrar Progresso")
        print("3. Ver Histórico de Progresso")
        print("4. Exibir Meus Treinos Salvos")
        print("5. Exibir Métricas de Saúde")  # Nova opção para exibir métricas de saúde
        print("6. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            gerar_planilha(usuario_id)
        elif escolha == "2":
            registrar_progresso(usuario_id)
        elif escolha == "3":
            ver_historico_progresso(usuario_id)
        elif escolha == "4":
            exibir_meus_treinos_salvos(usuario_id)
        elif escolha == "5":  # Chamar função para exibir métricas de saúde
            exibir_metricas_saude(usuario_id)
        elif escolha == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


def gerar_planilha(usuario_id):
    """Gera uma planilha de treino para o usuário."""
    print("\n=== GERAR PLANILHA DE TREINO ===")
    genero = input("Gênero (Masculino/Feminino): ")
    dias_disponiveis = int(input("Dias disponíveis para treinar (1-7): "))
    equipamentos = input("Acesso a equipamentos de academia? (Sim/Não): ")
    try:
        planilha_traduzida = iniciar_chatbot(usuario_id, genero, dias_disponiveis, equipamentos)
        print("\n=== PLANILHA DE TREINO RECOMENDADA ===")
        for dia, info in planilha_traduzida.items():
            grupo_muscular = info["grupo_muscular"]
            exercicios = info["exercicios"]
            print(f"\n=== {dia}: {grupo_muscular} ===")
            for i, exercicio in enumerate(exercicios, 1):
                print(f"{i}. {exercicio}")
    except Exception as e:
        print(f"Erro ao gerar planilha: {e}")


def registrar_progresso(usuario_id):
    """Registra o progresso do usuário."""
    print("\n=== REGISTRAR PROGRESSO ===")
    peso = float(input("Peso atual (kg): "))
    medidas_input = input("Medidas corporais (separadas por vírgulas): ")
    medidas = [m.strip() for m in medidas_input.split(",")] if medidas_input else []
    observacoes = input("Observações adicionais (opcional): ")
    try:
        salvar_progresso(usuario_id, peso, medidas, observacoes)
        print("Progresso registrado com sucesso!")
    except Exception as e:
        print(f"Erro ao registrar progresso: {e}")


def ver_historico_progresso(usuario_id):
    """Exibe o histórico de progresso do usuário."""
    print("\n=== HISTÓRICO DE PROGRESSO ===")
    historico = recuperar_historico_progresso(usuario_id)
    if not historico:
        print("Você ainda não registrou nenhum progresso.")
        return
    for registro in historico:
        print(f"\nData: {registro['data']}")
        print(f"Peso: {registro['peso']} kg")
        if registro['medidas']:
            print(f"Medidas: {', '.join(registro['medidas'])}")
        if registro['observacoes']:
            print(f"Observações: {registro['observacoes']}")


def exibir_meus_treinos_salvos(usuario_id):
    """Exibe os treinos salvos pelo usuário."""
    print("\n=== MEUS TREINOS SALVOS ===")
    treinos = exibir_meus_treinos(usuario_id)
    if not treinos:
        print("Você ainda não possui nenhum treino salvo.")
        return
    for data, exercicios in treinos:
        print(f"\nTreino - Data: {data}")
        for i, exercicio in enumerate(exercicios.split(", "), 1):
            print(f"{i}. {exercicio}")


def main():
    """Função principal para executar o sistema no terminal."""
    criar_banco_dados()
    while True:
        escolha = tela_inicial()
        if escolha == "1":  # Login
            usuario_id = tela_login()
            if usuario_id:
                menu_principal(usuario_id)
        elif escolha == "2":  # Cadastro
            tela_cadastro()
        elif escolha == "3":  # Sair
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()