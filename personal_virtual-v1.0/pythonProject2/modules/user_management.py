# modules/user_management.py

import sqlite3
import re
import hashlib

def criar_banco_dados():
    """
    Cria as tabelas no banco de dados SQLite, se elas ainda não existirem.
    """
    try:
        conexao = sqlite3.connect("data/users.db")
        cursor = conexao.cursor()

        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_usuario TEXT UNIQUE NOT NULL,
                email_ou_telefone TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                nome_preferido TEXT,
                idade INTEGER,
                peso REAL,
                altura REAL,
                nivel_experiencia TEXT,
                objetivo TEXT
            )
        """)

        # Tabela de treinos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS treinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                data DATE DEFAULT (date('now')),
                exercicios TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        """)

        # Tabela de progresso
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progresso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                data DATE DEFAULT (date('now')),
                peso REAL,
                medidas TEXT,
                observacoes TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        """)

        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conexao.close()

def validar_nome_usuario(nome_usuario):
    """
    Valida o nome de usuário.
    - Deve conter apenas letras, números e underline.
    - Deve ter entre 3 e 20 caracteres.
    """
    if not re.match(r"^[a-zA-Z0-9_]+$", nome_usuario):
        print("Erro: O nome de usuário deve conter apenas letras, números e underline.")
        return False
    if len(nome_usuario) < 3 or len(nome_usuario) > 20:
        print("Erro: O nome de usuário deve ter entre 3 e 20 caracteres.")
        return False
    return True

def validar_email_ou_telefone(email_ou_telefone):
    """
    Valida o e-mail ou telefone.
    - Se for e-mail, deve seguir o formato padrão.
    - Se for telefone, deve seguir o formato +XXXXXXXXXXX ou XXXXXXXXXX.
    """
    if "@" in email_ou_telefone:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_ou_telefone):
            print("Erro: E-mail inválido.")
            return False
    else:
        if not re.match(r"^\+?[0-9]{10,15}$", email_ou_telefone):
            print("Erro: Telefone inválido. Use o formato +XXXXXXXXXXX ou XXXXXXXXXX.")
            return False
    return True

def validar_senha(senha):
    """
    Valida a senha.
    - Deve ter pelo menos 6 caracteres.
    - Deve conter pelo menos uma letra maiúscula e um número.
    """
    if len(senha) < 6:
        print("Erro: A senha deve ter pelo menos 6 caracteres.")
        return False
    if not re.search(r"[A-Z]", senha):
        print("Erro: A senha deve conter pelo menos uma letra maiúscula.")
        return False
    if not re.search(r"[0-9]", senha):
        print("Erro: A senha deve conter pelo menos um número.")
        return False
    return True

def hash_senha(senha):
    """
    Criptografa a senha usando SHA-256.
    """
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario(nome_usuario, email_ou_telefone, senha, nome_preferido, idade, peso, altura, nivel_experiencia, objetivo):
    """
    Cadastra um novo usuário no banco de dados.
    """
    if not validar_nome_usuario(nome_usuario):
        return
    if not validar_email_ou_telefone(email_ou_telefone):
        return
    if not validar_senha(senha):
        return

    senha_hash = hash_senha(senha)
    try:
        conexao = sqlite3.connect("data/users.db")
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO usuarios (
                nome_usuario, email_ou_telefone, senha, nome_preferido, idade, peso, altura, nivel_experiencia, objetivo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome_usuario, email_ou_telefone, senha_hash, nome_preferido, idade, peso, altura, nivel_experiencia, objetivo))
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Nome de usuário ou e-mail/telefone já estão em uso.")
    finally:
        conexao.close()

def verificar_login(nome_usuario, senha):
    """
    Verifica as credenciais do usuário no banco de dados.
    """
    if not validar_nome_usuario(nome_usuario):
        return None

    senha_hash = hash_senha(senha)
    try:
        conexao = sqlite3.connect("data/users.db")
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT id FROM usuarios WHERE nome_usuario = ? AND senha = ?
        """, (nome_usuario, senha_hash))
        usuario = cursor.fetchone()
        return usuario[0] if usuario else None
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        conexao.close()

def recuperar_informacoes_usuario(usuario_id):
    """
    Recupera as informações do usuário com base no ID.
    """
    try:
        conexao = sqlite3.connect("data/users.db")
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT nome_preferido, idade, peso, altura, nivel_experiencia, objetivo
            FROM usuarios WHERE id = ?
        """, (usuario_id,))
        usuario = cursor.fetchone()
        return {
            "nome_preferido": usuario[0],
            "idade": usuario[1],
            "peso": usuario[2],
            "altura": usuario[3],
            "nivel_experiencia": usuario[4],
            "objetivo": usuario[5]
        } if usuario else None
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        conexao.close()

def salvar_treino(usuario_id, exercicios):
    """
    Salva os exercícios do treino no banco de dados.
    """
    try:
        conexao = sqlite3.connect("data/users.db")
        cursor = conexao.cursor()
        exercicios_str = ", ".join(exercicios)
        cursor.execute("""
            INSERT INTO treinos (usuario_id, exercicios)
            VALUES (?, ?)
        """, (usuario_id, exercicios_str))
        conexao.commit()
        print("Treino salvo com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao salvar treino: {e}")
    finally:
        conexao.close()

def exibir_meus_treinos(usuario_id):
    """
    Recupera os treinos salvos pelo usuário.
    """
    try:
        conexao = sqlite3.connect("data/users.db")
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT data, exercicios FROM treinos WHERE usuario_id = ? ORDER BY data DESC
        """, (usuario_id,))
        treinos = cursor.fetchall()
        return [(data, exercicios) for data, exercicios in treinos]
    except sqlite3.Error as e:
        print(f"Erro ao acessar treinos: {e}")
    finally:
        conexao.close()

def salvar_progresso(usuario_id, peso, medidas=None, observacoes=None):
    """
    Salva o progresso do usuário no banco de dados.
    """
    try:
        conexao = sqlite3.connect("data/users.db")
        cursor = conexao.cursor()
        medidas_str = ", ".join(medidas) if medidas else None
        cursor.execute("""
            INSERT INTO progresso (usuario_id, peso, medidas, observacoes)
            VALUES (?, ?, ?, ?)
        """, (usuario_id, peso, medidas_str, observacoes))
        conexao.commit()
        print("Progresso salvo com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao salvar progresso: {e}")
    finally:
        conexao.close()

def recuperar_historico_progresso(usuario_id):
    """
    Recupera o histórico de progresso do usuário.
    """
    try:
        conexao = sqlite3.connect("data/users.db")
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT data, peso, medidas, observacoes FROM progresso WHERE usuario_id = ? ORDER BY data ASC
        """, (usuario_id,))
        progresso = cursor.fetchall()
        historico = []
        for registro in progresso:
            data, peso, medidas, observacoes = registro
            historico.append({
                "data": data,
                "peso": peso,
                "medidas": medidas.split(", ") if medidas else [],
                "observacoes": observacoes
            })
        return historico
    except sqlite3.Error as e:
        print(f"Erro ao recuperar histórico: {e}")
    finally:
        conexao.close()