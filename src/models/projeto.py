import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'projetos.json')

STATUS_EM_FORMACAO = 'Em Formação'
STATUS_GRUPO_FECHADO = 'Grupo Fechado'


class Projeto:
    def __init__(self, titulo, resumo_tema, numero_vagas, criador_tipo,
                 criador_nome, status=STATUS_EM_FORMACAO, vagas_por_papel=None):
        self.titulo = titulo
        self.resumo_tema = resumo_tema
        self.numero_vagas = numero_vagas
        self.criador_tipo = criador_tipo
        self.criador_nome = criador_nome
        self.status = status
        self.participantes = []
        self.interessados = []
        self.data_criacao = None
        self.vagas_por_papel = vagas_por_papel or []  # list[{'papel': str, 'stack': str, 'quantidade': int}]

    def vagas_disponiveis(self):
        return self.numero_vagas - len(self.participantes)

    def to_dict(self):
        return {
            'titulo': self.titulo,
            'resumo_tema': self.resumo_tema,
            'numero_vagas': self.numero_vagas,
            'criador_tipo': self.criador_tipo,
            'criador_nome': self.criador_nome,
            'participantes': self.participantes,
            'status': self.status,
            'data_criacao': self.data_criacao,
            'interessados': self.interessados,
            'vagas_por_papel': self.vagas_por_papel,
        }


def carregar_projetos():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_projetos(projetos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(projetos, f, ensure_ascii=False, indent=2)


def estatisticas_projetos():
    projetos = carregar_projetos()
    em_formacao = [p for p in projetos if p['status'] == STATUS_EM_FORMACAO]
    vagas_disponiveis = sum(
        p['numero_vagas'] - len(p.get('participantes', []))
        for p in em_formacao
    )
    return {
        'total': len(projetos),
        'em_formacao': len(em_formacao),
        'grupo_fechado': len(projetos) - len(em_formacao),
        'vagas_disponiveis': vagas_disponiveis,
    }
