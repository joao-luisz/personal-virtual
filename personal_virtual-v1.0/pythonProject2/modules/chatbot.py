# modules/chatbot.py

import sys
import os

# Adicionar o diretório pai ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def iniciar_chatbot(usuario_id=None, genero="Masculino", dias_disponiveis=3, equipamentos="Sim"):
    """
    Função principal do chatbot para gerar uma planilha de treino.
    Recebe parâmetros diretamente da interface gráfica.
    """
    # Recuperar as informações do usuário do banco de dados
    informacoes_usuario = recuperar_informacoes_usuario(usuario_id)
    if not informacoes_usuario:
        return {"erro": "Não foi possível recuperar suas informações."}

    # Extrair informações do usuário
    nome_preferido = informacoes_usuario["nome_preferido"]
    idade = informacoes_usuario["idade"]
    peso = informacoes_usuario["peso"]
    altura = informacoes_usuario["altura"]
    nivel_experiencia = informacoes_usuario["nivel_experiencia"]
    objetivo = informacoes_usuario["objetivo"]

    # Gerar a planilha de treino
    print(f"\nRecomendando exercícios para {nome_preferido}...")
    planilha_treino = recomendar_exercicios_mega_gym(dias_disponiveis, equipamentos, genero, objetivo, nivel_experiencia)

    # Traduzir os exercícios da planilha
    planilha_traduzida = {}
    for dia, info in planilha_treino.items():
        grupo_muscular = info["grupo_muscular"]
        exercicios = info["exercicios"]
        exercicios_traduzidos = []
        for exercicio in exercicios:
            nome_exercicio = exercicio.split(" (")[0]
            traducao = traducoes.get(nome_exercicio, nome_exercicio)
            detalhes = f"{traducao} {exercicio.split(' (')[1]}"
            exercicios_traduzidos.append(detalhes)
        planilha_traduzida[dia] = {
            "grupo_muscular": grupo_muscular,
            "exercicios": exercicios_traduzidos
        }

    # Salvar o treino no banco de dados
    salvar_treino(usuario_id, [exercicio.split(" (")[0] for info in planilha_traduzida.values() for exercicio in info["exercicios"]])

    return planilha_traduzida


def registrar_progresso_gui(usuario_id, peso, medidas=None, observacoes=None):
    """
    Registra o progresso do usuário via interface gráfica.
    """
    try:
        salvar_progresso(usuario_id, peso, medidas, observacoes)
        return {"sucesso": "Progresso registrado com sucesso!"}
    except Exception as e:
        return {"erro": f"Erro ao registrar progresso: {e}"}


def recuperar_historico_progresso_gui(usuario_id):
    """
    Recupera o histórico de progresso do usuário para exibição na interface gráfica.
    """
    historico = recuperar_historico_progresso(usuario_id)
    if not historico:
        return {"erro": "Você ainda não registrou nenhum progresso."}

    # Formatar o histórico para exibição
    historico_formatado = []
    for registro in historico:
        data = registro['data']
        peso = registro['peso']
        medidas = ", ".join(registro['medidas']) if registro['medidas'] else "N/A"
        observacoes = registro['observacoes'] if registro['observacoes'] else "N/A"
        historico_formatado.append({
            "data": data,
            "peso": peso,
            "medidas": medidas,
            "observacoes": observacoes
        })

    return historico_formatado


def exibir_meus_treinos_gui(usuario_id):
    """
    Exibe os treinos salvos pelo usuário para exibição na interface gráfica.
    """
    treinos = exibir_meus_treinos(usuario_id)
    if not treinos:
        return {"erro": "Você ainda não possui nenhum treino salvo."}

    # Formatar os treinos para exibição
    treinos_formatados = []
    for data, exercicios in treinos:
        treinos_formatados.append({
            "data": data,
            "exercicios": exercicios.split(", ")
        })

    return treinos_formatados