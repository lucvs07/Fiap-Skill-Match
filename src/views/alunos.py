from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.views.dashboard import login_required
from src.models.aluno import carregar_alunos, NIVEIS_SKILL
from src.models.projeto import carregar_projetos
from src.models.convite import Convite, carregar_convites, salvar_convites

alunos_bp = Blueprint('alunos', __name__)


def _pode_buscar():
    if session.get('tipo') == 'mentor':
        return True
    nome = session.get('nome')
    return any(p.get('criador_nome') == nome for p in carregar_projetos())


@alunos_bp.route('/alunos')
@login_required
def busca_alunos():
    if not _pode_buscar():
        flash('Acesso restrito a mentores e criadores de projetos.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    skill_filtro = request.args.get('skill', '').strip().lower()
    nivel_filtro = request.args.get('nivel', '').strip()
    curso_filtro = request.args.get('curso', '').strip().lower()

    alunos = [a for a in carregar_alunos() if a.get('status_busca', 'fechado') == 'aberto']

    if skill_filtro:
        alunos = [
            a for a in alunos
            if any(skill_filtro in s['skill'].lower() for s in a.get('skills', []))
        ]
    if nivel_filtro and nivel_filtro in NIVEIS_SKILL:
        alunos = [
            a for a in alunos
            if any(s['nivel'] == nivel_filtro for s in a.get('skills', []))
        ]
    if curso_filtro:
        alunos = [a for a in alunos if curso_filtro in a.get('curso', '').lower()]

    return render_template(
        'alunos_busca.html',
        alunos=alunos,
        skill_filtro=skill_filtro,
        nivel_filtro=nivel_filtro,
        curso_filtro=curso_filtro,
        NIVEIS_SKILL=NIVEIS_SKILL,
    )


@alunos_bp.route('/alunos/<int:idx>')
@login_required
def perfil_publico(idx):
    if not _pode_buscar():
        flash('Acesso restrito a mentores e criadores de projetos.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    alunos = [a for a in carregar_alunos() if a.get('status_busca', 'fechado') == 'aberto']
    if idx < 0 or idx >= len(alunos):
        flash('Aluno não encontrado.', 'danger')
        return redirect(url_for('alunos.busca_alunos'))

    aluno = alunos[idx]
    nome = session.get('nome')
    meus_projetos = [p for p in carregar_projetos() if p.get('criador_nome') == nome]
    convites = carregar_convites()

    convites_enviados = {
        c['projeto_titulo']
        for c in convites
        if c['remetente'] == nome and c['destinatario'] == aluno['nome']
    }

    return render_template(
        'aluno_perfil_publico.html',
        aluno=aluno,
        aluno_idx=idx,
        meus_projetos=meus_projetos,
        convites_enviados=convites_enviados,
    )


@alunos_bp.route('/alunos/<int:idx>/convidar', methods=['POST'])
@login_required
def convidar(idx):
    if not _pode_buscar():
        flash('Acesso restrito a mentores e criadores de projetos.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    alunos = [a for a in carregar_alunos() if a.get('status_busca', 'fechado') == 'aberto']
    if idx < 0 or idx >= len(alunos):
        flash('Aluno não encontrado.', 'danger')
        return redirect(url_for('alunos.busca_alunos'))

    aluno = alunos[idx]
    projeto_titulo = request.form.get('projeto_titulo', '').strip()
    nome = session.get('nome')

    meus_projetos_titulos = {
        p['titulo'] for p in carregar_projetos() if p.get('criador_nome') == nome
    }
    if projeto_titulo not in meus_projetos_titulos:
        flash('Projeto inválido.', 'danger')
        return redirect(url_for('alunos.perfil_publico', idx=idx))

    convites = carregar_convites()
    ja_enviado = any(
        c['remetente'] == nome
        and c['destinatario'] == aluno['nome']
        and c['projeto_titulo'] == projeto_titulo
        for c in convites
    )
    if ja_enviado:
        flash('Convite já enviado para este aluno neste projeto.', 'info')
    else:
        convite = Convite(projeto_titulo, nome, aluno['nome'])
        convites.append(convite.to_dict())
        salvar_convites(convites)
        flash(f'Convite enviado para {aluno["nome"]}!', 'success')

    return redirect(url_for('alunos.perfil_publico', idx=idx))
