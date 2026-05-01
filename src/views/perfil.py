from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.views.dashboard import login_required
from src.models.aluno import carregar_alunos, salvar_alunos, NIVEIS_SKILL

perfil_bp = Blueprint('perfil', __name__)


@perfil_bp.route('/perfil')
@login_required
def perfil():
    if session.get('tipo') != 'aluno':
        return redirect(url_for('dashboard.dashboard'))
    aluno = next((a for a in carregar_alunos() if a['nome'] == session['nome']), None)
    return render_template('perfil.html', aluno=aluno)


@perfil_bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if session.get('tipo') != 'aluno':
        return redirect(url_for('dashboard.dashboard'))

    alunos = carregar_alunos()
    idx = next((i for i, a in enumerate(alunos) if a['nome'] == session['nome']), None)
    if idx is None:
        flash('Perfil não encontrado.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    aluno = alunos[idx]

    if request.method == 'POST':
        aluno['curso'] = request.form.get('curso', '').strip()
        aluno['areas_interesse'] = [
            a.strip() for a in request.form.get('areas_interesse', '').split(',') if a.strip()
        ]
        aluno['habilidades_tecnicas'] = [
            h.strip() for h in request.form.get('habilidades_tecnicas', '').split(',') if h.strip()
        ]

        skills_nomes = request.form.getlist('skill[]')
        skills_niveis = request.form.getlist('nivel[]')
        skills = []
        for nome, nivel in zip(skills_nomes, skills_niveis):
            nome = nome.strip()
            if nome and nivel in NIVEIS_SKILL:
                skills.append({'skill': nome, 'nivel': nivel})
        aluno['skills'] = skills

        aluno['links'] = {
            'github': request.form.get('github', '').strip(),
            'linkedin': request.form.get('linkedin', '').strip(),
            'figma': request.form.get('figma', '').strip(),
        }
        aluno['status_busca'] = request.form.get('status_busca', 'fechado')

        salvar_alunos(alunos)
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil.perfil'))

    return render_template('editar_perfil.html', aluno=aluno, NIVEIS_SKILL=NIVEIS_SKILL)
