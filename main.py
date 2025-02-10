import pandas as pd

# Banco de dados de exercícios (pré-definidos)
exercise_database = {
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
def user_registration():
    print("=== CADASTRO DE USUÁRIO ===")
    user_data = {}

    # Informações básicas
    user_data['nome'] = input("1. Nome (opcional): ").strip()
    user_data['idade'] = int(input("2. Idade: "))
    user_data['peso'] = float(input("3. Peso (kg): "))
    user_data['altura'] = float(input("4. Altura (cm): "))

    # Nível de experiência
    print("5. Nível de experiência:")
    print("[1] Iniciante [2] Intermediário [3] Avançado")
    experience_map = {1: 'Iniciante', 2: 'Intermediário', 3: 'Avançado'}
    user_data['nivel_experiencia'] = experience_map[int(input("Escolha uma opção (1-3): "))]

    return user_data


# Função para salvar os dados do usuário em uma planilha personalizada
def save_to_spreadsheet(user_data):
    # Define o nome do arquivo com base no nome do usuário
    file_name = f"{user_data['nome'].lower().replace(' ', '_')}.csv" if user_data['nome'] else "usuario.csv"

    # Criando um DataFrame com os dados do usuário
    df = pd.DataFrame([user_data])

    # Salvando os dados em um arquivo CSV
    try:
        # Verifica se o arquivo já existe
        existing_data = pd.read_csv(file_name)
        updated_data = pd.concat([existing_data, df], ignore_index=True)
        updated_data.to_csv(file_name, index=False)
    except FileNotFoundError:
        # Se o arquivo não existir, cria um novo
        df.to_csv(file_name, index=False)

    print(f"\nOs dados foram salvos na planilha '{file_name}'.")


# Função para recomendar exercícios
def recommend_exercises(user_data):
    nivel_experiencia = user_data['nivel_experiencia']
    exercises = exercise_database.get(nivel_experiencia, [])

    print("\n=== EXERCÍCIOS RECOMENDADOS ===")
    if exercises:
        for i, exercise in enumerate(exercises, 1):
            print(f"{i}. {exercise}")
    else:
        print("Nenhum exercício disponível para este nível.")


# Função para exibir uma mensagem personalizada
def display_message(user_data):
    print("\n=== RESUMO DO USUÁRIO ===")
    print(f"Olá, {user_data['nome'] or 'Usuário'}!")
    print(f"Idade: {user_data['idade']} anos")
    print(f"Peso: {user_data['peso']} kg")
    print(f"Altura: {user_data['altura']} cm")
    print(f"Nível de experiência: {user_data['nivel_experiencia']}")
    print("\nBem-vindo ao seu plano de treinos personalizado!")


# Executando o programa
if __name__ == "__main__":
    print("Bem-vindo ao Personal Trainer Virtual!")
    user_data = user_registration()
    save_to_spreadsheet(user_data)
    display_message(user_data)
    recommend_exercises(user_data)