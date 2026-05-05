# 🎓 Fiap Skill Match

## 📌 Descrição do Problema

A formação de squads para projetos de Iniciação Científica (IC) na FIAP é um processo informal e fragmentado. Alunos têm dificuldade em encontrar colegas com as habilidades certas para compor seu time, mentores não têm visibilidade sobre quem está disponível, e os projetos acabam sendo formados por contatos pessoais — excluindo talentos que simplesmente não estavam na rede certa.

Do outro lado, alunos com skills valorizadas ficam sem saber quais projetos precisam exatamente do que eles oferecem, e mentores não conseguem divulgar suas vagas de orientação de forma estruturada.

## 💡 Solução Proposta

O **Fiap Skill Match** é uma plataforma web que conecta alunos e mentores para a formação de squads em projetos de IC. O sistema permite:

- Publicar e descobrir projetos com vagas detalhadas por papel e stack tecnológica
- Manifestar interesse e ser aprovado como membro de um squad
- Enviar e receber convites diretos para projetos
- Mentores se candidatarem a projetos criados por alunos que precisam de orientação
- Alunos solicitarem mentoria de um mentor específico
- Buscar talentos por skill, nível e curso
- Acompanhar todos os projetos relacionados ao perfil em um só lugar

## 🆕 Evoluções do Checkpoint 1 para o Checkpoint 2

O Checkpoint 1 era uma aplicação de terminal com persistência em JSON, sem interface web, autenticação ou fluxo de interação entre usuários. O Checkpoint 2 representa uma reescrita completa da plataforma:

| Aspecto | Checkpoint 1 | Checkpoint 2 |
|---|---|---|
| Interface | Terminal (console) | Aplicação web com Flask e Bootstrap 5 |
| Autenticação | Nenhuma | Login/cadastro com sessão e bcrypt |
| Perfil de usuário | Não existia | Perfil completo com skills, links e status de busca |
| Projetos | Listagem simples | Mural com filtros, página de detalhe e aprovação de membros |
| Mentores | Listagem básica | Diretório com perfil público, candidatura a projetos e inbox de solicitações |
| Convites | Não existia | Fluxo completo: envio, inbox, aceitar/recusar com efeito no projeto |
| Visão do aluno | Não existia | Aba "Meus Projetos" separada por criados, participando e aguardando aprovação |
| Notificações | Não existia | Badge de convites pendentes na navbar para alunos e mentores |
| Busca de talentos | Não existia | Busca de alunos por skill, nível e curso aberta a todos os usuários |

## 🛠️ Tecnologias Utilizadas

- **Python 3** — linguagem principal
- **Flask 3** — framework web (rotas, sessões, blueprints, templates Jinja2)
- **Bootstrap 5** — interface responsiva via CDN
- **bcrypt** — hash seguro de senhas no cadastro
- **JSON** — persistência local de dados (alunos, mentores, projetos, convites)

## ⚙️ Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/lucvs07/Fiap-Skill-Match.git
cd Fiap-Skill-Match

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
flask --app src.app:create_app run --debug
```

Acesse em: [http://localhost:5000](http://localhost:5000)

## 📁 Estrutura do Projeto

```
Fiap-Skill-Match/
├── requirements.txt
└── src/
    ├── app.py                       # Factory da aplicação e context processors globais
    ├── auth/
    │   ├── cadastro.py              # Cadastro de alunos e mentores
    │   └── login.py                 # Login, logout e sessão
    ├── models/
    │   ├── aluno.py                 # Modelo e persistência de alunos
    │   ├── mentor.py                # Modelo e persistência de mentores
    │   ├── projeto.py               # Modelo e persistência de projetos
    │   ├── usuario.py               # Modelo base de usuário
    │   └── convite.py               # Modelo e persistência de convites
    ├── views/
    │   ├── dashboard.py             # Dashboard e decorator @login_required
    │   ├── perfil.py                # Perfil do aluno/mentor, convites e meus projetos
    │   ├── projetos.py              # Mural, detalhe, interesse, aprovação e mentoria
    │   ├── mentores.py              # Diretório, perfil público e solicitação de mentoria
    │   └── alunos.py                # Busca de talentos, perfil público e convites
    ├── data/
    │   ├── usuarios.json
    │   ├── alunos.json
    │   ├── mentores.json
    │   ├── projetos.json
    │   └── convites.json
    └── templates/
        ├── base.html                # Layout base com navbar e flash messages
        ├── login.html / cadastro.html
        ├── dashboard.html
        ├── projetos.html / novo_projeto.html / projeto_detalhe.html
        ├── mentores.html / mentor_detalhe.html
        ├── perfil.html / editar_perfil.html / perfil_mentor.html
        ├── alunos_busca.html / aluno_perfil_publico.html
        ├── convites.html / convites_mentor.html
        └── meus_projetos.html
```

## ✅ Funcionalidades Implementadas

### Cadastro e Login

- Cadastro separado para **Aluno** e **Mentor** com campos específicos por tipo de usuário
- Senha armazenada com hash bcrypt
- Login com sessão Flask e proteção de rotas via decorator `@login_required`
- Logout com limpeza de sessão
- Redirecionamento automático conforme tipo de usuário (aluno/mentor)

### Casos de Uso

| Caso de Uso | Status |
|---|---|
| Cadastro e login de aluno | ✅ Implementado |
| Cadastro e login de mentor | ✅ Implementado |
| Edição de perfil do aluno (skills, links, áreas de interesse, status de busca) | ✅ Implementado |
| Perfil interno do mentor com projetos e estatísticas | ✅ Implementado |
| Publicar projeto com vagas por papel e stack tecnológica | ✅ Implementado |
| Marcar projeto como "precisa de mentor" na criação | ✅ Implementado |
| Mural de projetos com filtros por status, papel e busca textual | ✅ Implementado |
| Página de detalhe do projeto com métricas de vagas e participantes | ✅ Implementado |
| Aluno manifesta interesse em projeto | ✅ Implementado |
| Criador aprova ou recusa interessados individualmente | ✅ Implementado |
| Fechamento automático do grupo ao atingir limite de vagas | ✅ Implementado |
| Mentor se candidata a projetos de alunos que precisam de orientação | ✅ Implementado |
| Aluno aprova ou recusa candidatura de mentor ao projeto | ✅ Implementado |
| Envio de convite de squad por mentor ou criador de projeto para aluno | ✅ Implementado |
| Aluno solicita mentoria diretamente no perfil de um mentor | ✅ Implementado |
| Inbox de convites do aluno com aceitar/recusar e efeito no projeto | ✅ Implementado |
| Inbox de solicitações de mentoria do mentor com aceitar/recusar | ✅ Implementado |
| Badge de notificação de convites pendentes na navbar (aluno e mentor) | ✅ Implementado |
| Busca de alunos por skill, nível e curso (aberta a todos os usuários) | ✅ Implementado |
| Perfil público do aluno com skills e opção de convite para squad | ✅ Implementado |
| Diretório de mentores com filtros por disponibilidade e especialidade | ✅ Implementado |
| Perfil público do mentor com projetos, contato e solicitação de mentoria | ✅ Implementado |
| Aba "Meus Projetos" do aluno (criados, participando, aguardando aprovação) | ✅ Implementado |
| Dashboard com estatísticas gerais e projetos recentes | ✅ Implementado |

## ⭐ Diferencial do Projeto

### Descrição

O diferencial do Fiap Skill Match é o **fluxo bidirecional de conexão entre alunos e mentores**. Ao contrário de plataformas que apenas listam projetos abertos, o sistema viabiliza quatro caminhos distintos de formação de squad:

1. **Aluno → Projeto**: manifesta interesse em um projeto e aguarda aprovação do criador
2. **Criador → Aluno**: envia convite diretamente para um aluno encontrado na busca de talentos
3. **Mentor → Projeto**: se candidata a projetos de alunos que precisam de orientação
4. **Aluno → Mentor**: solicita mentoria de um mentor específico direto do perfil público dele

Todos os fluxos passam por uma etapa de aprovação, dando controle a quem criou o projeto ou recebeu a solicitação. Isso evita squads formados ao acaso e aproxima o processo da dinâmica real de formação de times de pesquisa acadêmica.

### Justificativa

A formação de squads por afinidade pessoal tende a reproduzir vieses de rede — quem conhece mais pessoas tem vantagem sobre quem tem mais habilidades. Um sistema estruturado com busca por skill e fluxos de candidatura cria igualdade de acesso às oportunidades, independentemente do networking prévio do aluno ou do mentor.

### Referências

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- FIAP — Graduação em Engenharia de Software, 2025

## 🎬 Demonstração

- [Vídeo de apresentação — Checkpoint 1](https://www.youtube.com/watch?v=Sdnw7jtl4P0)
- [Vídeo de apresentação — Checkpoint 2](https://youtu.be/EfwtMyMiHK0)

## 👥 Integrantes do Grupo

| Nome | RM |
|---|---|
| Lucas Rodrigues Grecco | RM 558261 |
| Monique Ferreira dos Anjos | RM 558262 |
| Tiago Brito Nário | RM 558248 |
| Felipe Wapf Fettback | RM 557217 |
| Leonardo Tanaka Cortez | RM 556781 |
| Rafael Augusto Oliveira Silva | RM 555154 |

## 🔗 Links

- [Repositório GitHub](https://github.com/lucvs07/Fiap-Skill-Match)
- [Miro — Mapeamento do Projeto](https://miro.com/welcomeonboard/OWc5ZHh0ZVpQVEg2S2laUHFEYzZmN0kxMVh5QldsUlJmTVIxWkVVd21pSUdDRGtKNGF6UDgxM3A4VjZMUWtaWVNvQjAwS01rcFBPT3g1OC9OajBkVlFiVmtvckVBWURpSjJ1YVVZVHZvOVBBdkovclZUU2svak42L1FueDR3KzRzVXVvMm53MW9OWFg1bkJoVXZxdFhRPT0hdjE=?share_link_id=595511452638)
- [Vídeo de Apresentação — CP1](https://www.youtube.com/watch?v=Sdnw7jtl4P0)
- [Vídeo de apresentação — Checkpoint 2](https://youtu.be/EfwtMyMiHK0)
