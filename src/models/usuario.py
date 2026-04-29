import json
import os
import bcrypt

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.json')


class Usuario:
    def __init__(self, nome, email, senha_hash, tipo):
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.tipo = tipo  # 'aluno' ou 'mentor'

    def set_senha(self, senha):
        self.senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    def verificar_senha(self, senha):
        return bcrypt.checkpw(senha.encode(), self.senha_hash.encode())

    def to_dict(self):
        return {
            'nome': self.nome,
            'email': self.email,
            'senha_hash': self.senha_hash,
            'tipo': self.tipo,
        }


def carregar_usuarios():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_usuarios(usuarios):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)


def buscar_por_email(email):
    return next((u for u in carregar_usuarios() if u['email'] == email), None)
