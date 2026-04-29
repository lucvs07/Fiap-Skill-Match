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
    projetos = carregar_projetos()
    busca = request.args.get('busca', '').strip().lower()
    status_filtro = request.args.get('status', '')

    if busca:
        projetos = [p for p in projetos if busca in p['titulo'].lower()
                    or busca in p['resumo_tema'].lower()]
    if status_filtro in (STATUS_EM_FORMACAO, STATUS_GRUPO_FECHADO):
        projetos = [p for p in projetos if p['status'] == status_filtro]

    return render_template(
        'projetos.html',
        projetos=projetos,
        busca=busca,
        status_filtro=status_filtro,
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
            tipo = session.get('tipo', 'aluno').capitalize()
            projeto = Projeto(titulo, resumo, int(vagas), tipo, session.get('nome'))
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
