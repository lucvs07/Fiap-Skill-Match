from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, flash
from src.models.aluno import carregar_alunos
from src.models.mentor import carregar_mentores
from src.models.projeto import carregar_projetos, estatisticas_projetos

dashboard_bp = Blueprint('dashboard', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Faça login primeiro.', 'warning')
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'alunos': len(carregar_alunos()),
        'mentores': len(carregar_mentores()),
        **estatisticas_projetos(),
    }
    todos_projetos = carregar_projetos()
    projetos_recentes = todos_projetos[-3:][::-1]
    nome = session.get('nome')
    tem_projetos = any(p.get('criador_nome') == nome for p in todos_projetos)
    return render_template(
        'dashboard.html',
        nome=nome,
        tipo=session.get('tipo'),
        stats=stats,
        projetos_recentes=projetos_recentes,
        tem_projetos=tem_projetos,
    )
