from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd

# Inicializar o aplicativo Flask
app = Flask(__name__, static_folder='static')  # Define a pasta 'static' para arquivos do front-end
CORS(app)  # Permitir todas as origens para testes locais

# Carregar o dataset com verificação de erro
try:
    dataset = pd.read_csv('gym_exercise_data_clean.csv')
    print("Dataset carregado com sucesso!")
except FileNotFoundError:
    print("Erro: 'gym_exercise_data_clean.csv' não encontrado!")
    dataset = pd.DataFrame()

# Rota para servir a página inicial
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# Rota para gerar recomendações de treino
@app.route('/recommend', methods=['POST'])
def recommend():
    if dataset.empty:
        return jsonify({"error": "Dataset não carregado"}), 500

    preferences = request.json
    muscle_group = preferences.get('muscle_group')
    equipment = preferences.get('equipment')

    filtered = dataset[
        (dataset['BodyPart'].str.contains(muscle_group, case=False, na=False)) &
        (dataset['Equipment'].str.contains(equipment, case=False, na=False))
    ]

    if len(filtered) == 0:
        return jsonify({"message": "Nenhum exercício encontrado para essa combinação"}), 200

    recommendations = filtered.sample(min(5, len(filtered))).to_dict('records')
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)