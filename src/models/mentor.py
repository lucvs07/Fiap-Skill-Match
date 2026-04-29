import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'mentores.json')

DISPONIBILIDADES = ('Alta', 'Média', 'Baixa')


class Mentor:
    def __init__(self, nome, departamento, linhas_pesquisa, disponibilidade,
                 email, especialidades):
        self.nome = nome
        self.departamento = departamento
        self.linhas_pesquisa = linhas_pesquisa    # list[str]
        self.disponibilidade = disponibilidade    # 'Alta' | 'Média' | 'Baixa'
        self.email = email
        self.especialidades = especialidades      # list[str]
        self.alunos_orientando = []

    def to_dict(self):
        return {
            'nome': self.nome,
            'departamento': self.departamento,
            'linhas_pesquisa': self.linhas_pesquisa,
            'disponibilidade': self.disponibilidade,
            'email': self.email,
            'especialidades': self.especialidades,
            'alunos_orientando': self.alunos_orientando,
        }


def carregar_mentores():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_mentores(mentores):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(mentores, f, ensure_ascii=False, indent=2)


def buscar_mentor_por_nome(nome):
    return next((m for m in carregar_mentores() if m['nome'] == nome), None)
