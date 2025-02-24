# modules/health_metrics.py

import sqlite3

def calcular_imc(peso, altura):
    """
    Calcula o Índice de Massa Corporal (IMC).
    Fórmula: IMC = peso (kg) / (altura (m) ** 2)
    """
    altura_metros = altura / 100  # Converter altura de cm para metros
    imc = peso / (altura_metros ** 2)
    return round(imc, 2)

def classificar_imc(imc):
    """
    Classifica o IMC em categorias.
    """
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        return "Peso normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidade"

def calcular_tmb(peso, altura, idade, genero, nivel_atividade):
    """
    Calcula a Taxa Metabólica Basal (TMB).
    Fórmulas baseadas no gênero e ajustadas pelo nível de atividade.
    """
    if genero.lower() == "masculino":
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade)
    elif genero.lower() == "feminino":
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * idade)
    else:
        raise ValueError("Gênero inválido. Escolha 'Masculino' ou 'Feminino'.")

    # Ajustar TMB com base no nível de atividade
    fatores_atividade = {
        "sedentario": 1.2,
        "leve": 1.375,
        "moderado": 1.55,
        "ativo": 1.725,
        "muito ativo": 1.9
    }
    if nivel_atividade not in fatores_atividade:
        raise ValueError("Nível de atividade inválido. Escolha entre 'sedentario', 'leve', 'moderado', 'ativo' ou 'muito ativo'.")

    return round(tmb * fatores_atividade[nivel_atividade], 2)

def calcular_agua_recomendada(peso, nivel_atividade):
    """
    Calcula a quantidade de água recomendada com base no peso e nível de atividade.
    Fórmula: Água (litros) = peso (kg) * fator_atividade
    """
    fatores_atividade = {
        "sedentario": 0.035,
        "leve": 0.040,
        "moderado": 0.045,
        "ativo": 0.050,
        "muito ativo": 0.055
    }
    if nivel_atividade not in fatores_atividade:
        raise ValueError("Nível de atividade inválido. Escolha entre 'sedentario', 'leve', 'moderado', 'ativo' ou 'muito ativo'.")

    return round(peso * fatores_atividade[nivel_atividade], 2)

def exibir_metricas_saude(usuario_id):
    try:
        # Conectar ao banco de dados
        conexao = sqlite3.connect("data/users.db")
        cursor = conexao.cursor()

        # Selecionar as métricas de saúde do usuário
        cursor.execute("""
            SELECT nome_preferido, peso, altura, idade, genero, nivel_atividade 
            FROM usuarios WHERE id = ?
        """, (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            print("Usuário não encontrado.")
            return

        nome_preferido, peso, altura, idade, genero, nivel_atividade = usuario

        # Calcular métricas de saúde
        imc = calcular_imc(peso, altura)
        classificacao_imc = classificar_imc(imc)
        tmb = calcular_tmb(peso, altura, idade, genero, nivel_atividade)
        agua = calcular_agua_recomendada(peso, nivel_atividade)

        # Exibir as métricas
        print(f"\n=== MÉTRICAS DE SAÚDE DE {nome_preferido.upper()} ===")
        print(f"IMC: {imc} ({classificacao_imc})")
        print(f"TMB: {tmb} kcal/dia")
        print(f"Água Recomendada: {agua} litros/dia")

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        # Fechar a conexão
        if 'conexao' in locals():
            conexao.close()