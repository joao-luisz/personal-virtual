# modules/workout_recommendation.py

import pandas as pd

def filtrar_exercicios_validos(df):
    """
    Filtra o dataset para incluir apenas nomes de exercícios válidos.
    """
    # Lista de palavras-chave comuns em nomes de exercícios
    palavras_chave = [
        "push", "pull", "squat", "press", "curl", "fly", "deadlift", "lunge",
        "plank", "row", "extension", "raise", "dip", "crunch", "bridge", "kick",
        "hold", "jack", "jump", "swing", "mountain", "burpee", "leg", "arm",
        "shoulder", "chest", "back", "core", "abs", "glute", "hamstring", "quad"
    ]
    # Filtrar exercícios cujo título contenha pelo menos uma palavra-chave
    df_filtrado = df[df["Title"].str.lower().apply(
        lambda x: any(palavra in x for palavra in palavras_chave)
    )]
    # Incluir exercícios com descrições claras no campo "BodyPart"
    df_filtrado = pd.concat([
        df_filtrado,
        df[df["BodyPart"].isin(["Chest", "Back", "Quads", "Calves", "Hamstrings", "Glutes", "Shoulders", "Biceps", "Triceps", "Abs"])]
    ]).drop_duplicates()
    return df_filtrado

def definir_series_repeticoes(objetivo, nivel_experiencia):
    if nivel_experiencia == "Iniciante":
        series = 2 if objetivo == "emagrecimento" else 3
        repeticoes = "12-15"
    elif nivel_experiencia == "Intermediário":
        series = 3 if objetivo == "emagrecimento" else 4
        repeticoes = "10-12"
    else:  # Avançado
        series = 4 if objetivo == "emagrecimento" else 5
        repeticoes = "8-10"
    return {"series": series, "repeticoes": repeticoes}

def distribuir_grupos_musculares(dias_disponiveis):
    grupos_base = [
        "Peito + Triceps",
        "Costas + Biceps",
        "Quadriceps + Panturrilha",
        "Posterior de Coxa + Gluteos",
        "Ombros + Triceps",
        "Abdomen",
        "Cardio"
    ]
    return [grupos_base[i % len(grupos_base)] for i in range(dias_disponiveis)]

def recomendar_exercicios_mega_gym(dias_disponiveis, equipamentos, genero, objetivo, nivel_experiencia):
    # Carregar o dataset MegaGymDataset.csv
    try:
        df = pd.read_csv("data/megaGymDataset.csv")
    except FileNotFoundError:
        print("Erro: O arquivo 'megaGymDataset.csv' não foi encontrado.")
        return {}
    except Exception as e:
        print(f"Erro ao carregar o dataset: {e}")
        return {}

    # Filtrar exercícios válidos
    df = filtrar_exercicios_validos(df)

    # Filtrar exercícios com base na disponibilidade de equipamentos
    if equipamentos == "Sim":
        exercicios_filtrados = df[df["Equipment"] != "None"]
    else:
        exercicios_filtrados = df[df["Equipment"] == "None"]

    # Mapear exercícios para grupos musculares
    grupos_musculares = {
        "Peito": ["Chest"],
        "Costas": ["Back"],
        "Quadriceps": ["Quads"],
        "Panturrilha": ["Calves"],
        "Posterior de Coxa": ["Hamstrings"],
        "Gluteos": ["Glutes"],
        "Ombros": ["Shoulders"],
        "Biceps": ["Biceps"],
        "Triceps": ["Triceps"],
        "Abdomen": ["Abs"]
    }

    # Definir séries e repetições
    series_repeticoes = definir_series_repeticoes(objetivo, nivel_experiencia)

    # Definir os dias de treino
    dias_da_semana = [
        "Segunda-feira", "Terça-feira", "Quarta-feira",
        "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
    ]

    # Criar a planilha de treino
    planilha_treino = {}
    grupo_muscular_map = distribuir_grupos_musculares(dias_disponiveis)
    for i in range(dias_disponiveis):
        dia = dias_da_semana[i]
        grupo_muscular = grupo_muscular_map[i]
        musculos = []
        for grupo in grupo_muscular.split(" + "):
            musculos.extend(grupos_musculares.get(grupo, []))
        # Filtrar exercícios para o grupo muscular do dia
        exercicios_grupo = exercicios_filtrados[
            exercicios_filtrados["BodyPart"].isin(musculos)
        ]
        # Selecionar até 5 exercícios para o dia
        if not exercicios_grupo.empty:
            exercicios_selecionados = exercicios_grupo.sample(min(5, len(exercicios_grupo)))["Title"].tolist()
        else:
            exercicios_selecionados = ["Descanso"]
        # Adicionar as séries e repetições a cada exercício
        exercicios_com_detalhes = [
            f"{exercicio} ({series_repeticoes['series']} séries x {series_repeticoes['repeticoes']} repetições)"
            for exercicio in exercicios_selecionados
        ]
        # Adicionar o grupo muscular à planilha
        planilha_treino[dia] = {
            "grupo_muscular": grupo_muscular,
            "exercicios": exercicios_com_detalhes
        }
    return planilha_treino