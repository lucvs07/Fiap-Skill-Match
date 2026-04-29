import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'alunos.json')


class Aluno:
    def __init__(self, nome, curso, areas_interesse, habilidades_tecnicas):
        self.nome = nome
        self.curso = curso
        self.areas_interesse = areas_interesse      # list[str]
        self.habilidades_tecnicas = habilidades_tecnicas  # list[str]

    def to_dict(self):
        return {
            'nome': self.nome,
            'curso': self.curso,
            'areas_interesse': self.areas_interesse,
            'habilidades_tecnicas': self.habilidades_tecnicas,
        }


def carregar_alunos():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_alunos(alunos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(alunos, f, ensure_ascii=False, indent=2)


def buscar_aluno_por_nome(nome):
    return next((a for a in carregar_alunos() if a['nome'] == nome), None)
