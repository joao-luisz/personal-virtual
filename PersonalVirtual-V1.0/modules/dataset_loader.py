# modules/dataset_loader.py

import pandas as pd
import os

def carregar_dataset(caminho_dataset="data/megaGymDataset.csv"):
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_dataset):
        print(f"Erro: O arquivo '{caminho_dataset}' não foi encontrado.")
        return None

    # Tentar carregar o dataset com diferentes codificações
    codificacoes = ['utf-8-sig', 'latin1', 'iso-8859-1']
    for codificacao in codificacoes:
        try:
            dataset = pd.read_csv(caminho_dataset, encoding=codificacao)
            break
        except Exception as e:
            print(f"Tentando outra codificação... Erro: {e}")
    else:
        print("Erro: Não foi possível carregar o dataset com nenhuma das codificações testadas.")
        return None

    # Verificar se o dataset está vazio
    if dataset.empty:
        print("Erro: O dataset está vazio.")
        return None

    # Verificar se as colunas obrigatórias estão presentes
    colunas_obrigatorias = ["Exercise Name", "Type", "Muscle", "Equipment", "Level"]
    if not all(col in dataset.columns for col in colunas_obrigatorias):
        print("Erro: O dataset não contém todas as colunas obrigatórias.")
        return None

    # Exibir as primeiras linhas do dataset para depuração
    print("Primeiras linhas do dataset:")
    print(dataset.head())
    print("Dataset carregado com sucesso!")

    return dataset
