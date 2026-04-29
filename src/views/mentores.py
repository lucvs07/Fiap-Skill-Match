from flask import Blueprint, render_template, request
from src.views.dashboard import login_required
from src.models.mentor import carregar_mentores, DISPONIBILIDADES

mentores_bp = Blueprint('mentores', __name__)


@mentores_bp.route('/mentores')
@login_required
def diretorio():
    mentores = carregar_mentores()
    disponibilidade_filtro = request.args.get('disponibilidade', '')
    busca = request.args.get('busca', '').strip().lower()

    if disponibilidade_filtro in DISPONIBILIDADES:
        mentores = [m for m in mentores if m['disponibilidade'] == disponibilidade_filtro]
    if busca:
        mentores = [
            m for m in mentores
            if busca in m['nome'].lower()
            or busca in m['departamento'].lower()
            or any(busca in e.lower() for e in m.get('especialidades', []))
            or any(busca in l.lower() for l in m.get('linhas_pesquisa', []))
        ]

    return render_template(
        'mentores.html',
        mentores=mentores,
        busca=busca,
        disponibilidade_filtro=disponibilidade_filtro,
        disponibilidades=DISPONIBILIDADES,
    )


@mentores_bp.route('/mentores/<int:idx>')
@login_required
def detalhe(idx):
    mentores = carregar_mentores()
    if idx < 0 or idx >= len(mentores):
        return render_template('mentores.html',
                               mentores=carregar_mentores(),
                               busca='', disponibilidade_filtro='',
                               disponibilidades=DISPONIBILIDADES), 404
    return render_template('mentor_detalhe.html', mentor=mentores[idx], idx=idx)
