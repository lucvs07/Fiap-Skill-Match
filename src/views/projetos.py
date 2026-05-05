from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.views.dashboard import login_required
from src.models.projeto import (
    Projeto, carregar_projetos, salvar_projetos,
    STATUS_EM_FORMACAO, STATUS_GRUPO_FECHADO,
)

projetos_bp = Blueprint('projetos', __name__)


@projetos_bp.route('/projetos')
@login_required
def mural():
    todos = carregar_projetos()
    busca = request.args.get('busca', '').strip().lower()
    status_filtro = request.args.get('status', '')
    papel_filtro = request.args.get('papel', '').strip()

    projetos_com_idx = list(enumerate(todos))
    if busca:
        projetos_com_idx = [(i, p) for i, p in projetos_com_idx
                            if busca in p['titulo'].lower() or busca in p['resumo_tema'].lower()]
    if status_filtro in (STATUS_EM_FORMACAO, STATUS_GRUPO_FECHADO):
        projetos_com_idx = [(i, p) for i, p in projetos_com_idx if p['status'] == status_filtro]
    if papel_filtro:
        projetos_com_idx = [
            (i, p) for i, p in projetos_com_idx
            if any(v['papel'].lower() == papel_filtro.lower()
                   for v in p.get('vagas_por_papel', []))
        ]

    papeis = sorted({
        v['papel']
        for p in todos
        for v in p.get('vagas_por_papel', [])
        if v.get('papel')
    })

    return render_template(
        'projetos.html',
        projetos_com_idx=projetos_com_idx,
        busca=busca,
        status_filtro=status_filtro,
        papel_filtro=papel_filtro,
        papeis=papeis,
        STATUS_EM_FORMACAO=STATUS_EM_FORMACAO,
        STATUS_GRUPO_FECHADO=STATUS_GRUPO_FECHADO,
    )


@projetos_bp.route('/projetos/novo', methods=['GET', 'POST'])
@login_required
def novo_projeto():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        resumo = request.form.get('resumo_tema', '').strip()
        vagas = request.form.get('numero_vagas', '').strip()

        if not titulo:
            flash('Título é obrigatório.', 'danger')
        elif not resumo:
            flash('Resumo do tema é obrigatório.', 'danger')
        elif not vagas.isdigit() or int(vagas) < 1:
            flash('Número de vagas deve ser um inteiro positivo.', 'danger')
        else:
            papeis_nomes = request.form.getlist('papel[]')
            papeis_stacks = request.form.getlist('stack[]')
            papeis_qtds = request.form.getlist('quantidade[]')
            vagas_por_papel = []
            for p, s, q in zip(papeis_nomes, papeis_stacks, papeis_qtds):
                p = p.strip()
                if p:
                    try:
                        qtd = int(q) if q.strip().isdigit() else 1
                    except (ValueError, AttributeError):
                        qtd = 1
                    vagas_por_papel.append({'papel': p, 'stack': s.strip(), 'quantidade': qtd})

            tipo = session.get('tipo', 'aluno').capitalize()
            project_dict = Projeto(titulo, resumo, int(vagas), tipo, session.get('nome'),
                                   vagas_por_papel=vagas_por_papel).to_dict()
            project_dict['precisa_mentor'] = 'precisa_mentor' in request.form
            projetos = carregar_projetos()
            projetos.append(project_dict)
            salvar_projetos(projetos)
            flash('Projeto publicado com sucesso!', 'success')
            return redirect(url_for('projetos.mural'))

    return render_template('novo_projeto.html')


@projetos_bp.route('/projetos/<int:idx>')
@login_required
def detalhe(idx):
    projetos = carregar_projetos()
    if idx < 0 or idx >= len(projetos):
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('projetos.mural'))
    projeto = projetos[idx]
    eh_criador = (session.get('nome') == projeto.get('criador_nome')
                  and session.get('tipo') == projeto.get('criador_tipo', '').lower())
    return render_template('projeto_detalhe.html', projeto=projeto, idx=idx,
                           eh_criador=eh_criador,
                           STATUS_EM_FORMACAO=STATUS_EM_FORMACAO,
                           STATUS_GRUPO_FECHADO=STATUS_GRUPO_FECHADO)


@projetos_bp.route('/projetos/<int:idx>/status', methods=['POST'])
@login_required
def alterar_status(idx):
    projetos = carregar_projetos()
    if idx < 0 or idx >= len(projetos):
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('projetos.mural'))
    projeto = projetos[idx]
    eh_criador = (session.get('nome') == projeto.get('criador_nome')
                  and session.get('tipo') == projeto.get('criador_tipo', '').lower())
    if not eh_criador:
        flash('Sem permissão.', 'danger')
        return redirect(url_for('projetos.detalhe', idx=idx))
    novo_status = request.form.get('status')
    if novo_status in (STATUS_EM_FORMACAO, STATUS_GRUPO_FECHADO):
        projeto['status'] = novo_status
        salvar_projetos(projetos)
        flash(f'Status atualizado para "{novo_status}".', 'success')
    return redirect(url_for('projetos.detalhe', idx=idx))


@projetos_bp.route('/projetos/<int:idx>/aprovar/<nome>', methods=['POST'])
@login_required
def aprovar_interessado(idx, nome):
    projetos = carregar_projetos()
    if idx < 0 or idx >= len(projetos):
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('projetos.mural'))
    projeto = projetos[idx]
    if session.get('nome') != projeto.get('criador_nome'):
        flash('Sem permissão.', 'danger')
        return redirect(url_for('projetos.detalhe', idx=idx))
    if nome in projeto.get('interessados', []) and nome not in projeto.get('participantes', []):
        projeto['interessados'].remove(nome)
        projeto.setdefault('participantes', []).append(nome)
        vagas_restantes = projeto['numero_vagas'] - len(projeto['participantes'])
        if vagas_restantes <= 0:
            projeto['status'] = STATUS_GRUPO_FECHADO
        salvar_projetos(projetos)
        flash(f'{nome} aprovado(a) como participante.', 'success')
    return redirect(url_for('projetos.detalhe', idx=idx))


@projetos_bp.route('/projetos/<int:idx>/rejeitar/<nome>', methods=['POST'])
@login_required
def rejeitar_interessado(idx, nome):
    projetos = carregar_projetos()
    if idx < 0 or idx >= len(projetos):
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('projetos.mural'))
    projeto = projetos[idx]
    if session.get('nome') != projeto.get('criador_nome'):
        flash('Sem permissão.', 'danger')
        return redirect(url_for('projetos.detalhe', idx=idx))
    if nome in projeto.get('interessados', []):
        projeto['interessados'].remove(nome)
        salvar_projetos(projetos)
        flash(f'Interesse de {nome} recusado.', 'info')
    return redirect(url_for('projetos.detalhe', idx=idx))


@projetos_bp.route('/projetos/<int:idx>/interesse', methods=['POST'])
@login_required
def manifestar_interesse(idx):
    if session.get('tipo') != 'aluno':
        flash('Apenas alunos podem manifestar interesse.', 'warning')
        return redirect(url_for('projetos.mural'))

    projetos = carregar_projetos()
    if idx < 0 or idx >= len(projetos):
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('projetos.mural'))

    projeto = projetos[idx]
    nome = session.get('nome')

    if projeto['status'] == STATUS_GRUPO_FECHADO:
        flash('Este projeto já está com o grupo fechado.', 'warning')
    elif nome in projeto.get('interessados', []):
        flash('Você já manifestou interesse neste projeto.', 'info')
    elif nome in projeto.get('participantes', []):
        flash('Você já é participante deste projeto.', 'info')
    else:
        projeto.setdefault('interessados', []).append(nome)
        salvar_projetos(projetos)
        flash(f'Interesse em "{projeto["titulo"]}" registrado!', 'success')

    return redirect(url_for('projetos.detalhe', idx=idx))


@projetos_bp.route('/projetos/<int:idx>/candidatar-mentor', methods=['POST'])
@login_required
def candidatar_mentor(idx):
    if session.get('tipo') != 'mentor':
        flash('Apenas mentores podem se candidatar.', 'warning')
        return redirect(url_for('projetos.detalhe', idx=idx))

    projetos = carregar_projetos()
    if idx < 0 or idx >= len(projetos):
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('projetos.mural'))

    projeto = projetos[idx]
    nome = session.get('nome')

    if not projeto.get('precisa_mentor'):
        flash('Este projeto não precisa de mentor.', 'warning')
    elif projeto.get('criador_tipo', '').lower() != 'aluno':
        flash('Apenas projetos criados por alunos aceitam candidatura de mentor.', 'warning')
    elif projeto.get('mentor_responsavel'):
        flash('Este projeto já tem um mentor responsável.', 'warning')
    elif nome in projeto.get('mentores_interessados', []):
        flash('Você já enviou sua candidatura para este projeto.', 'info')
    else:
        projeto.setdefault('mentores_interessados', []).append(nome)
        salvar_projetos(projetos)
        flash('Candidatura enviada com sucesso!', 'success')

    return redirect(url_for('projetos.detalhe', idx=idx))


@projetos_bp.route('/projetos/<int:idx>/aprovar-mentor/<nome>', methods=['POST'])
@login_required
def aprovar_mentor(idx, nome):
    projetos = carregar_projetos()
    if idx < 0 or idx >= len(projetos):
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('projetos.mural'))

    projeto = projetos[idx]
    if session.get('nome') != projeto.get('criador_nome'):
        flash('Sem permissão.', 'danger')
        return redirect(url_for('projetos.detalhe', idx=idx))

    if nome in projeto.get('mentores_interessados', []):
        projeto['mentor_responsavel'] = nome
        projeto['mentores_interessados'] = []
        salvar_projetos(projetos)
        flash(f'{nome} aprovado(a) como mentor responsável.', 'success')
    else:
        flash('Candidatura não encontrada.', 'danger')

    return redirect(url_for('projetos.detalhe', idx=idx))


@projetos_bp.route('/projetos/<int:idx>/rejeitar-mentor/<nome>', methods=['POST'])
@login_required
def rejeitar_mentor(idx, nome):
    projetos = carregar_projetos()
    if idx < 0 or idx >= len(projetos):
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('projetos.mural'))

    projeto = projetos[idx]
    if session.get('nome') != projeto.get('criador_nome'):
        flash('Sem permissão.', 'danger')
        return redirect(url_for('projetos.detalhe', idx=idx))

    if nome in projeto.get('mentores_interessados', []):
        projeto['mentores_interessados'].remove(nome)
        salvar_projetos(projetos)
        flash(f'Candidatura de {nome} recusada.', 'info')
    else:
        flash('Candidatura não encontrada.', 'danger')

    return redirect(url_for('projetos.detalhe', idx=idx))
