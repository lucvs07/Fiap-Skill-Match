import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'convites.json')


class Convite:
    def __init__(self, projeto_titulo, remetente, destinatario,
                 status='pendente', data=None):
        self.projeto_titulo = projeto_titulo
        self.remetente = remetente        # nome do usuário que convida
        self.destinatario = destinatario  # nome do aluno convidado
        self.status = status              # 'pendente' | 'aceito' | 'recusado'
        self.data = data or datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    def to_dict(self):
        return {
            'projeto_titulo': self.projeto_titulo,
            'remetente': self.remetente,
            'destinatario': self.destinatario,
            'status': self.status,
            'data': self.data,
        }


def carregar_convites():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_convites(convites):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(convites, f, ensure_ascii=False, indent=2)
