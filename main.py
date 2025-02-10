import pandas as pd

# Banco de dados de exercícios (pré-definidos)
banco_de_exercicios = {
    "Iniciante": [
        "Flexão de braço (Push-up)",
        "Agachamento (Squat)",
        "Abdominal básico",
        "Polichinelo",
        "Prancha (Plank)"
    ],
    "Intermediário": [
        "Flexão diamante",
        "Agachamento com salto",
        "Abdominal bicicleta",
        "Burpee",
        "Mountain Climber"
    ],
    "Avançado": [
        "Flexão explosiva (Clap Push-up)",
        "Agachamento com peso",
        "Abdominal canivete",
        "Pular corda intensivo",
        "Handstand Push-up"
    ]
}

# Função para o formulário de cadastro
def formulario_cadastro():
    print("=== CADASTRO DE USUÁRIO ===")
    dados_usuario = {}

    # Informações básicas
    dados_usuario['nome'] = input("1. Nome (opcional): ").strip()
    dados_usuario['idade'] = int(input("2. Idade: "))
    dados_usuario['peso'] = float(input("3. Peso (kg): "))
    dados_usuario['altura'] = float(input("4. Altura (cm): "))

    # Nível de experiência
    print("5. Nível de experiência:")
    print("[1] Iniciante [2] Intermediário [3] Avançado")
    mapa_nivel = {1: 'Iniciante', 2: 'Intermediário', 3: 'Avançado'}
    dados_usuario['nivel_experiencia'] = mapa_nivel[int(input("Escolha uma opção (1-3): "))]

    return dados_usuario

# Função para salvar os dados do usuário em uma planilha personalizada
def salvar_planilha(dados_usuario):
    # Define o nome do arquivo com base no nome do usuário
    nome_arquivo = f"{dados_usuario['nome'].lower().replace(' ', '_')}.csv" if dados_usuario['nome'] else "usuario.csv"
    
    # Criando um DataFrame com os dados do usuário
    df = pd.DataFrame([dados_usuario])

    # Salvando os dados em um arquivo CSV
    try:
        # Verifica se o arquivo já existe
        dados_existentes = pd.read_csv(nome_arquivo)
        dados_atualizados = pd.concat([dados_existentes, df], ignore_index=True)
        dados_atualizados.to_csv(nome_arquivo, index=False)
    except FileNotFoundError:
        # Se o arquivo não existir, cria um novo
        df.to_csv(nome_arquivo, index=False)

    print(f"\nOs dados foram salvos na planilha '{nome_arquivo}'.")

# Função para recomendar exercícios
def recomendar_exercicios(dados_usuario):
    nivel_experiencia = dados_usuario['nivel_experiencia']
    exercicios = banco_de_exercicios.get(nivel_experiencia, [])

    print("\n=== EXERCÍCIOS RECOMENDADOS ===")
    if exercicios:
        for i, exercicio in enumerate(exercicios, 1):
            print(f"{i}. {exercicio}")
    else:
        print("Nenhum exercício disponível para este nível.")

# Função para exibir uma mensagem personalizada
def exibir_mensagem_personalizada(dados_usuario):
    print("\n=== RESUMO DO USUÁRIO ===")
    print(f"Olá, {dados_usuario['nome'] or 'Usuário'}!")
    print(f"Idade: {dados_usuario['idade']} anos")
    print(f"Peso: {dados_usuario['peso']} kg")
    print(f"Altura: {dados_usuario['altura']} cm")
    print(f"Nível de experiência: {dados_usuario['nivel_experiencia']}")
    print("\nBem-vindo ao seu plano de treinos personalizado!")

# Executando o programa
if __name__ == "__main__":
    print("Bem-vindo ao Personal Trainer Virtual!")
    dados_usuario = formulario_cadastro()
    salvar_planilha(dados_usuario)
    exibir_mensagem_personalizada(dados_usuario)
    recomendar_exercicios(dados_usuario)
