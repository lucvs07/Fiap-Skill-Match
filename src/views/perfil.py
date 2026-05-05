from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.views.dashboard import login_required
from src.models.aluno import carregar_alunos, salvar_alunos, NIVEIS_SKILL
from src.models.mentor import carregar_mentores
from src.models.projeto import carregar_projetos, salvar_projetos, STATUS_GRUPO_FECHADO
from src.models.convite import carregar_convites, salvar_convites

perfil_bp = Blueprint('perfil', __name__)


@perfil_bp.route('/perfil')
@login_required
def perfil():
    if session.get('tipo') == 'mentor':
        return redirect(url_for('perfil.perfil_mentor'))
    if session.get('tipo') != 'aluno':
        return redirect(url_for('dashboard.dashboard'))
    aluno = next((a for a in carregar_alunos() if a['nome'] == session['nome']), None)
    return render_template('perfil.html', aluno=aluno)


@perfil_bp.route('/perfil/mentor')
@login_required
def perfil_mentor():
    if session.get('tipo') != 'mentor':
        return redirect(url_for('perfil.perfil'))
    mentor = next((m for m in carregar_mentores() if m['nome'] == session['nome']), None)
    todos_projetos = carregar_projetos()
    projetos_com_idx = [(i, p) for i, p in enumerate(todos_projetos)
                        if p.get('criador_nome') == session['nome']]
    return render_template('perfil_mentor.html', mentor=mentor, projetos_com_idx=projetos_com_idx)


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


@perfil_bp.route('/perfil/projetos')
@login_required
def meus_projetos():
    if session.get('tipo') != 'aluno':
        return redirect(url_for('dashboard.dashboard'))
    nome = session.get('nome')
    todos = carregar_projetos()
    criados = [(i, p) for i, p in enumerate(todos) if p.get('criador_nome') == nome]
    participando = [(i, p) for i, p in enumerate(todos)
                    if nome in p.get('participantes', []) and p.get('criador_nome') != nome]
    interessado = [(i, p) for i, p in enumerate(todos)
                   if nome in p.get('interessados', [])]
    return render_template('meus_projetos.html',
                           criados=criados,
                           participando=participando,
                           interessado=interessado)


@perfil_bp.route('/convites')
@login_required
def convites():
    if session.get('tipo') != 'aluno':
        return redirect(url_for('dashboard.dashboard'))
    nome = session.get('nome')
    todos = carregar_convites()
    meus_convites = [(i, c) for i, c in enumerate(todos) if c['destinatario'] == nome]
    return render_template('convites.html', convites_com_idx=meus_convites)


@perfil_bp.route('/convites/<int:idx>/aceitar', methods=['POST'])
@login_required
def aceitar_convite(idx):
    if session.get('tipo') != 'aluno':
        return redirect(url_for('dashboard.dashboard'))
    nome = session.get('nome')
    convites = carregar_convites()
    if idx < 0 or idx >= len(convites) or convites[idx]['destinatario'] != nome:
        flash('Convite não encontrado.', 'danger')
        return redirect(url_for('perfil.convites'))
    convite = convites[idx]
    if convite['status'] != 'pendente':
        flash('Este convite já foi respondido.', 'info')
        return redirect(url_for('perfil.convites'))

    projetos = carregar_projetos()
    projeto = next((p for p in projetos if p['titulo'] == convite['projeto_titulo']), None)
    if projeto and nome not in projeto.get('participantes', []):
        projeto.setdefault('participantes', []).append(nome)
        projeto.setdefault('interessados', [])
        if nome in projeto['interessados']:
            projeto['interessados'].remove(nome)
        vagas_restantes = projeto['numero_vagas'] - len(projeto['participantes'])
        if vagas_restantes <= 0:
            projeto['status'] = STATUS_GRUPO_FECHADO
        salvar_projetos(projetos)

    convite['status'] = 'aceito'
    salvar_convites(convites)
    flash(f'Convite para "{convite["projeto_titulo"]}" aceito!', 'success')
    return redirect(url_for('perfil.convites'))


@perfil_bp.route('/convites/<int:idx>/recusar', methods=['POST'])
@login_required
def recusar_convite(idx):
    if session.get('tipo') != 'aluno':
        return redirect(url_for('dashboard.dashboard'))
    nome = session.get('nome')
    convites = carregar_convites()
    if idx < 0 or idx >= len(convites) or convites[idx]['destinatario'] != nome:
        flash('Convite não encontrado.', 'danger')
        return redirect(url_for('perfil.convites'))
    convite = convites[idx]
    if convite['status'] != 'pendente':
        flash('Este convite já foi respondido.', 'info')
        return redirect(url_for('perfil.convites'))
    convite['status'] = 'recusado'
    salvar_convites(convites)
    flash(f'Convite para "{convite["projeto_titulo"]}" recusado.', 'info')
    return redirect(url_for('perfil.convites'))


@perfil_bp.route('/convites/mentor')
@login_required
def convites_mentor():
    if session.get('tipo') != 'mentor':
        return redirect(url_for('dashboard.dashboard'))
    nome = session.get('nome')
    todos = carregar_convites()
    meus_convites = [(i, c) for i, c in enumerate(todos) if c['destinatario'] == nome]
    return render_template('convites_mentor.html', convites_com_idx=meus_convites)


@perfil_bp.route('/convites/<int:idx>/aceitar-mentor', methods=['POST'])
@login_required
def aceitar_convite_mentor(idx):
    if session.get('tipo') != 'mentor':
        return redirect(url_for('dashboard.dashboard'))
    nome = session.get('nome')
    convites = carregar_convites()
    if idx < 0 or idx >= len(convites) or convites[idx]['destinatario'] != nome:
        flash('Convite não encontrado.', 'danger')
        return redirect(url_for('perfil.convites_mentor'))
    convite = convites[idx]
    if convite['status'] != 'pendente':
        flash('Este convite já foi respondido.', 'info')
        return redirect(url_for('perfil.convites_mentor'))

    projetos = carregar_projetos()
    projeto = next((p for p in projetos if p['titulo'] == convite['projeto_titulo']), None)
    if projeto:
        projeto['mentor_responsavel'] = nome
        projeto['mentores_interessados'] = []
        salvar_projetos(projetos)

    convite['status'] = 'aceito'
    salvar_convites(convites)
    flash(f'Solicitação de mentoria para "{convite["projeto_titulo"]}" aceita!', 'success')
    return redirect(url_for('perfil.convites_mentor'))


@perfil_bp.route('/convites/<int:idx>/recusar-mentor', methods=['POST'])
@login_required
def recusar_convite_mentor(idx):
    if session.get('tipo') != 'mentor':
        return redirect(url_for('dashboard.dashboard'))
    nome = session.get('nome')
    convites = carregar_convites()
    if idx < 0 or idx >= len(convites) or convites[idx]['destinatario'] != nome:
        flash('Convite não encontrado.', 'danger')
        return redirect(url_for('perfil.convites_mentor'))
    convite = convites[idx]
    if convite['status'] != 'pendente':
        flash('Este convite já foi respondido.', 'info')
        return redirect(url_for('perfil.convites_mentor'))
    convite['status'] = 'recusado'
    salvar_convites(convites)
    flash(f'Solicitação de mentoria para "{convite["projeto_titulo"]}" recusada.', 'info')
    return redirect(url_for('perfil.convites_mentor'))
