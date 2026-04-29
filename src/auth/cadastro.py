import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.usuario import Usuario, carregar_usuarios, salvar_usuarios, buscar_por_email
from src.models.aluno import Aluno, carregar_alunos, salvar_alunos
from src.models.mentor import Mentor, carregar_mentores, salvar_mentores, DISPONIBILIDADES

cadastro_bp = Blueprint('cadastro', __name__)


def _email_valido(email):
    return re.match(r'^[\w.+-]+@[\w-]+\.[a-z]{2,}$', email, re.IGNORECASE)


def _senha_valida(senha):
    return len(senha) >= 8


def _lista_from_campo(valor):
    return [item.strip() for item in valor.split(',') if item.strip()]


def _validar_campos_comuns(nome, email, senha):
    if not nome:
        return 'Nome é obrigatório.'
    if not _email_valido(email):
        return 'E-mail inválido.'
    if not _senha_valida(senha):
        return 'Senha deve ter pelo menos 8 caracteres.'
    if buscar_por_email(email):
        return 'E-mail já cadastrado.'
    return None


def _registrar_aluno(nome, form):
    curso = form.get('curso', '').strip()
    areas = _lista_from_campo(form.get('areas_interesse', ''))
    habilidades = _lista_from_campo(form.get('habilidades_tecnicas', ''))

    if not curso:
        return 'Curso é obrigatório.'
    if not areas:
        return 'Informe pelo menos uma área de interesse.'
    if not habilidades:
        return 'Informe pelo menos uma habilidade técnica.'

    aluno = Aluno(nome, curso, areas, habilidades)
    alunos = carregar_alunos()
    alunos.append(aluno.to_dict())
    salvar_alunos(alunos)
    return None


def _registrar_mentor(nome, email, form):
    departamento = form.get('departamento', '').strip()
    linhas = _lista_from_campo(form.get('linhas_pesquisa', ''))
    disponibilidade = form.get('disponibilidade', 'Média')
    especialidades = _lista_from_campo(form.get('especialidades', ''))

    if not departamento:
        return 'Departamento é obrigatório.'
    if not linhas:
        return 'Informe pelo menos uma linha de pesquisa.'
    if disponibilidade not in DISPONIBILIDADES:
        return 'Disponibilidade inválida.'
    if not especialidades:
        return 'Informe pelo menos uma especialidade.'

    mentor = Mentor(nome, departamento, linhas, disponibilidade, email, especialidades)
    mentores = carregar_mentores()
    mentores.append(mentor.to_dict())
    salvar_mentores(mentores)
    return None


@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = request.form
    if request.method == 'POST':
        nome = form.get('nome', '').strip()
        email = form.get('email', '').strip()
        senha = form.get('senha', '')
        tipo = form.get('tipo', 'aluno')

        erro = _validar_campos_comuns(nome, email, senha)
        if not erro:
            if tipo == 'aluno':
                erro = _registrar_aluno(nome, form)
            else:
                erro = _registrar_mentor(nome, email, form)

        if erro:
            flash(erro, 'danger')
        else:
            usuario = Usuario(nome, email, '', tipo)
            usuario.set_senha(senha)
            usuarios = carregar_usuarios()
            usuarios.append(usuario.to_dict())
            salvar_usuarios(usuarios)
            flash('Cadastro realizado! Faça login.', 'success')
            return redirect(url_for('login.login'))

    return render_template('cadastro.html', disponibilidades=DISPONIBILIDADES)
