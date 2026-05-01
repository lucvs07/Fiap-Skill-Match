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

    projetos = todos
    if busca:
        projetos = [p for p in projetos if busca in p['titulo'].lower()
                    or busca in p['resumo_tema'].lower()]
    if status_filtro in (STATUS_EM_FORMACAO, STATUS_GRUPO_FECHADO):
        projetos = [p for p in projetos if p['status'] == status_filtro]
    if papel_filtro:
        projetos = [
            p for p in projetos
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
        projetos=projetos,
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
            projeto = Projeto(titulo, resumo, int(vagas), tipo, session.get('nome'),
                              vagas_por_papel=vagas_por_papel)
            projetos = carregar_projetos()
            projetos.append(projeto.to_dict())
            salvar_projetos(projetos)
            flash('Projeto publicado com sucesso!', 'success')
            return redirect(url_for('projetos.mural'))

    return render_template('novo_projeto.html')


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

    return redirect(url_for('projetos.mural'))
