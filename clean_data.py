import pandas as pd

# Carregar o dataset original
df = pd.read_csv('megaGymDataset.csv')

# Verificar as colunas disponíveis
print("Colunas do dataset:", df.columns.tolist())

# Remover linhas com valores nulos nas colunas essenciais
essential_columns = ['Title', 'BodyPart', 'Equipment']
df = df.dropna(subset=essential_columns)

# Converter texto para minúsculas para consistência
for col in essential_columns:
    df[col] = df[col].str.lower()

# Remover duplicatas baseadas no nome do exercício
df = df.drop_duplicates(subset=['Title'])

# Selecionar apenas colunas úteis
df_clean = df[['Title', 'BodyPart', 'Equipment']]

# Salvar o dataset limpo
df_clean.to_csv('gym_exercise_data_clean.csv', index=False)

print("Dataset limpo salvo como 'gym_exercise_data_clean.csv'")
print("Número de linhas após limpeza:", len(df_clean))