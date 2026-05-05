from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.views.dashboard import login_required
from src.models.mentor import carregar_mentores, DISPONIBILIDADES
from src.models.projeto import carregar_projetos
from src.models.convite import Convite, carregar_convites, salvar_convites

mentores_bp = Blueprint('mentores', __name__)


@mentores_bp.route('/mentores')
@login_required
def diretorio():
    todos_mentores = carregar_mentores()
    disponibilidade_filtro = request.args.get('disponibilidade', '')
    busca = request.args.get('busca', '').strip().lower()

    def passes_filters(m):
        if disponibilidade_filtro in DISPONIBILIDADES and m['disponibilidade'] != disponibilidade_filtro:
            return False
        if busca and not (
            busca in m['nome'].lower()
            or busca in m['departamento'].lower()
            or any(busca in e.lower() for e in m.get('especialidades', []))
            or any(busca in l.lower() for l in m.get('linhas_pesquisa', []))
        ):
            return False
        return True

    mentores_com_idx = [(i, m) for i, m in enumerate(todos_mentores) if passes_filters(m)]

    return render_template(
        'mentores.html',
        mentores_com_idx=mentores_com_idx,
        busca=busca,
        disponibilidade_filtro=disponibilidade_filtro,
        disponibilidades=DISPONIBILIDADES,
    )


@mentores_bp.route('/mentores/<int:idx>')
@login_required
def detalhe(idx):
    mentores = carregar_mentores()
    if idx < 0 or idx >= len(mentores):
        todos_mentores = carregar_mentores()
        mentores_com_idx = list(enumerate(todos_mentores))
        return render_template('mentores.html',
                               mentores_com_idx=mentores_com_idx,
                               busca='', disponibilidade_filtro='',
                               disponibilidades=DISPONIBILIDADES), 404
    mentor = mentores[idx]
    todos_projetos = carregar_projetos()
    projetos_mentor = [
        p for p in todos_projetos
        if p.get('criador_nome') == mentor['nome']
    ]

    projetos_para_solicitar = []
    if session.get('tipo') == 'aluno':
        todos = carregar_projetos()
        ja_solicitados = {
            c['projeto_titulo'] for c in carregar_convites()
            if c['remetente'] == session.get('nome') and c['destinatario'] == mentor['nome']
        }
        projetos_para_solicitar = [
            p for p in todos
            if p.get('criador_nome') == session.get('nome')
            and p.get('precisa_mentor')
            and not p.get('mentor_responsavel')
            and p['titulo'] not in ja_solicitados
        ]

    return render_template('mentor_detalhe.html', mentor=mentor, idx=idx,
                           projetos=projetos_mentor,
                           projetos_para_solicitar=projetos_para_solicitar)


@mentores_bp.route('/mentores/<int:idx>/solicitar', methods=['POST'])
@login_required
def solicitar_mentoria(idx):
    if session.get('tipo') != 'aluno':
        flash('Apenas alunos podem solicitar mentoria.', 'warning')
        return redirect(url_for('mentores.detalhe', idx=idx))

    mentores = carregar_mentores()
    if idx < 0 or idx >= len(mentores):
        flash('Mentor não encontrado.', 'danger')
        return redirect(url_for('mentores.diretorio'))

    mentor = mentores[idx]
    projeto_titulo = request.form.get('projeto_titulo', '').strip()
    nome = session.get('nome')

    todos = carregar_projetos()
    projeto = next(
        (p for p in todos
         if p.get('criador_nome') == nome and p['titulo'] == projeto_titulo),
        None
    )

    if not projeto:
        flash('Projeto inválido.', 'danger')
        return redirect(url_for('mentores.detalhe', idx=idx))
    if not projeto.get('precisa_mentor'):
        flash('Este projeto não precisa de mentor.', 'warning')
        return redirect(url_for('mentores.detalhe', idx=idx))
    if projeto.get('mentor_responsavel'):
        flash('Este projeto já tem um mentor responsável.', 'warning')
        return redirect(url_for('mentores.detalhe', idx=idx))

    convites = carregar_convites()
    ja_enviado = any(
        c['remetente'] == nome
        and c['destinatario'] == mentor['nome']
        and c['projeto_titulo'] == projeto_titulo
        for c in convites
    )
    if ja_enviado:
        flash('Solicitação já enviada para este mentor neste projeto.', 'info')
    else:
        convite = Convite(projeto_titulo, nome, mentor['nome'])
        convites.append(convite.to_dict())
        salvar_convites(convites)
        flash(f'Solicitação de mentoria enviada para {mentor["nome"]}!', 'success')

    return redirect(url_for('mentores.detalhe', idx=idx))
