
# Classe para representar um aluno
class Aluno:
	def __init__(self, nome, curso, areas_interesse, habilidades_tecnicas=None):
		self.nome = nome
		self.curso = curso
		self.areas_interesse = areas_interesse  # lista de strings
		self.habilidades_tecnicas = habilidades_tecnicas or []  # stacks técnicas

	def __repr__(self):
		return f"Aluno(nome={self.nome}, curso={self.curso}, areas_interesse={self.areas_interesse}, habilidades={self.habilidades_tecnicas})"


# Classe para representar um mentor (professor) - RF02
class Mentor:
	def __init__(self, nome, departamento, linhas_pesquisa, disponibilidade, email=None, especialidades=None):
		self.nome = nome
		self.departamento = departamento
		self.linhas_pesquisa = linhas_pesquisa  # lista de linhas de pesquisa
		self.disponibilidade = disponibilidade  # "Alta", "Média", "Baixa"
		self.email = email
		self.especialidades = especialidades or []  # áreas de especialidade técnica
		self.alunos_orientando = []  # lista de alunos que o mentor está orientando
	
	def adicionar_aluno(self, aluno):
		"""Adiciona um aluno à lista de orientandos"""
		if aluno not in self.alunos_orientando:
			self.alunos_orientando.append(aluno)
			return True
		return False
	
	def remover_aluno(self, aluno):
		"""Remove um aluno da lista de orientandos"""
		if aluno in self.alunos_orientando:
			self.alunos_orientando.remove(aluno)
			return True
		return False
	
	def __repr__(self):
		return f"Mentor(nome={self.nome}, departamento={self.departamento}, linhas_pesquisa={self.linhas_pesquisa}, disponibilidade={self.disponibilidade})"


# Classe para representar um projeto - RF03
class Projeto:
	def __init__(self, titulo, resumo_tema, numero_vagas, criador):
		self.titulo = titulo
		self.resumo_tema = resumo_tema
		self.numero_vagas = numero_vagas
		self.criador = criador  # pode ser Mentor ou Aluno
		self.participantes = []  # lista de alunos participantes
		self.status = "Em Formação"  # status do projeto: "Em Formação" ou "Grupo Fechado"
		self.data_criacao = None  # data de criação do projeto
		self.interessados = []  # lista de alunos interessados - RF06
	
	def adicionar_participante(self, aluno):
		"""Adiciona um aluno como participante do projeto"""
		if aluno not in self.participantes:
			self.participantes.append(aluno)
			return True
		return False
	
	def remover_participante(self, aluno):
		"""Remove um aluno da lista de participantes"""
		if aluno in self.participantes:
			self.participantes.remove(aluno)
			return True
		return False
	
	def vagas_disponiveis(self):
		"""Retorna o número de vagas disponíveis"""
		return self.numero_vagas - len(self.participantes)
	
	def esta_cheio(self):
		"""Verifica se o projeto está com todas as vagas preenchidas"""
		return self.vagas_disponiveis() <= 0
	
	def marcar_em_formacao(self):
		"""Marca o projeto como em formação (vagas abertas)"""
		self.status = "Em Formação"

	def marcar_grupo_fechado(self):
		"""Marca o projeto como grupo fechado (IC iniciada)"""
		self.status = "Grupo Fechado"

	def adicionar_interessado(self, aluno):
		"""Adiciona um aluno à lista de interessados - RF06"""
		if aluno not in self.interessados:
			self.interessados.append(aluno)
			return True
		return False
	
	def __repr__(self):
		tipo_criador = "Mentor" if isinstance(self.criador, Mentor) else "Aluno"
		return f"Projeto(titulo={self.titulo}, resumo={self.resumo_tema[:50]}..., vagas={self.numero_vagas}, status={self.status}, criador={tipo_criador} {self.criador.nome})"


# Classe para gerenciar o Mural de Projetos - RF04
class MuralDeProjetos:
	def __init__(self):
		self.projetos_lista = []  # referência à lista de projetos global
	
	def definir_projetos(self, projetos_lista):
		"""Define a lista de projetos a ser gerenciada"""
		self.projetos_lista = projetos_lista
	
	def obter_projetos_em_formacao(self):
		"""Retorna apenas os projetos com status 'Em Formação'"""
		return [p for p in self.projetos_lista if p.status == "Em Formação"]
	
	def obter_projetos_com_vagas(self):
		"""Retorna projetos em formação que ainda possuem vagas disponíveis"""
		return [p for p in self.projetos_lista if p.vagas_disponiveis() > 0 and p.status == "Em Formação"]
	
	def filtrar_por_tema(self, palavra_chave):
		"""Filtra projetos por palavra-chave no título ou resumo"""
		palavra_chave = palavra_chave.lower()
		return [p for p in self.obter_projetos_em_formacao() 
				if palavra_chave in p.titulo.lower() or palavra_chave in p.resumo_tema.lower()]
	
	def filtrar_por_criador_tipo(self, tipo):
		"""Filtra projetos por tipo de criador ('Mentor' ou 'Aluno')"""
		if tipo.lower() == 'mentor':
			return [p for p in self.obter_projetos_em_formacao() if isinstance(p.criador, Mentor)]
		elif tipo.lower() == 'aluno':
			return [p for p in self.obter_projetos_em_formacao() if isinstance(p.criador, Aluno)]
		return self.obter_projetos_em_formacao()
	
	def contar_projetos_abertos(self):
		"""Retorna a quantidade de projetos em formação"""
		return len(self.obter_projetos_em_formacao())
	
	def contar_vagas_totais_disponiveis(self):
		"""Retorna o total de vagas disponíveis em todos os projetos em formação"""
		return sum(p.vagas_disponiveis() for p in self.obter_projetos_em_formacao())
	
	def exibir_mural_resumido(self):
		"""Exibe o mural de projetos de forma resumida e rápida"""
		projetos_abertos = self.obter_projetos_em_formacao()
		
		if not projetos_abertos:
			print("\n" + "="*70)
			print("MURAL DE PROJETOS - NENHUM PROJETO EM FORMAÇÃO")
			print("="*70)
			print("Não há projetos de IC em formação no momento.")
			return
		
		print("\n" + "="*70)
		print("MURAL DE PROJETOS - RF04")
		print("="*70)
		print(f"Total de projetos em formação: {len(projetos_abertos)}")
		print(f"Total de vagas disponíveis: {self.contar_vagas_totais_disponiveis()}")
		print("="*70)
		
		for idx, projeto in enumerate(projetos_abertos, 1):
			tipo_criador = "👨‍🏫 Mentor" if isinstance(projeto.criador, Mentor) else "👨‍🎓 Aluno"
			status_vagas = f"({projeto.vagas_disponiveis()} vagas disponíveis)" if projeto.vagas_disponiveis() > 0 else "(VAGAS CHEIAS)"
			
			print(f"\n[{idx}] {projeto.titulo}")
			print(f"    📌 Criador: {projeto.criador.nome} ({tipo_criador})")
			print(f"    📝 Tema: {projeto.resumo_tema}")
			print(f"    👥 Vagas: {projeto.numero_vagas} total {status_vagas}")
			print(f"    ➕ Participantes: {len(projeto.participantes)}")
	
	def exibir_mural_detalhado(self):
		"""Exibe o mural de projetos com informações detalhadas"""
		projetos_abertos = self.obter_projetos_em_formacao()
		
		if not projetos_abertos:
			print("\n" + "="*70)
			print("MURAL DE PROJETOS - NENHUM PROJETO EM FORMAÇÃO")
			print("="*70)
			return
		
		print("\n" + "="*70)
		print("MURAL DE PROJETOS - VISUALIZAÇÃO DETALHADA - RF04")
		print("="*70)
		
		for idx, projeto in enumerate(projetos_abertos, 1):
			tipo_criador = "Mentor" if isinstance(projeto.criador, Mentor) else "Aluno"
			print(f"\n{'─'*70}")
			print(f"║ PROJETO #{idx} ║")
			print(f"{'─'*70}")
			print(f"Título:          {projeto.titulo}")
			print(f"Tema:            {projeto.resumo_tema}")
			print(f"Criador:         {projeto.criador.nome}")
			print(f"Tipo Criador:    {tipo_criador}")
			
			if isinstance(projeto.criador, Mentor):
				print(f"Departamento:    {projeto.criador.departamento}")
				print(f"Disponibilidade: {projeto.criador.disponibilidade}")
				if projeto.criador.email:
					print(f"Email Contato:   {projeto.criador.email}")
			else:
				print(f"Curso Aluno:     {projeto.criador.curso}")
			
			print(f"Vagas Totais:    {projeto.numero_vagas}")
			print(f"Vagas Ocupadas:  {len(projeto.participantes)}")
			print(f"Vagas Livres:    {projeto.vagas_disponiveis()}")
			print(f"Status:          {projeto.status}")
			
			if projeto.participantes:
				print(f"Participantes Atuais:")
				for p in projeto.participantes:
					print(f"  • {p.nome} ({p.curso})")
			
			if projeto.interessados:
				print(f"Alunos Interessados:")
				for i in projeto.interessados:
					print(f"  • {i.nome} ({i.curso})")
		
		print(f"\n{'='*70}")
	
	def exibir_mural_com_filtro(self, palavra_chave):
		"""Exibe o mural filtrado por palavra-chave"""
		projetos_filtrados = self.filtrar_por_tema(palavra_chave)
		
		if not projetos_filtrados:
			print(f"\nNenhum projeto encontrado com '{palavra_chave}'")
			return
		
		print(f"\n{'='*70}")
		print(f"RESULTADOS DA BUSCA - '{palavra_chave}'")
		print(f"Total encontrado: {len(projetos_filtrados)} projeto(s)")
		print(f"{'='*70}")
		
		for idx, projeto in enumerate(projetos_filtrados, 1):
			tipo_criador = "👨‍🏫 Mentor" if isinstance(projeto.criador, Mentor) else "👨‍🎓 Aluno"
			print(f"\n[{idx}] {projeto.titulo}")
			print(f"    📌 Criador: {projeto.criador.nome} ({tipo_criador})")
			print(f"    📝 Tema: {projeto.resumo_tema}")
			print(f"    👥 Vagas disponíveis: {projeto.vagas_disponiveis()} de {projeto.numero_vagas}")


# Classe para gerenciar o Diretório de Mentores - RF05
class DiretorioMentores:
	def __init__(self):
		self.mentores_lista = []

	def definir_mentores(self, mentores_lista):
		"""Define a lista de mentores a ser gerenciada"""
		self.mentores_lista = mentores_lista

	def obter_mentores_disponiveis(self):
		"""Retorna mentores com disponibilidade para orientar"""
		return [m for m in self.mentores_lista if m.disponibilidade in ("Alta", "Média")]

	def filtrar_por_especialidade(self, palavra_chave):
		"""Filtra mentores por especialidade técnica"""
		palavra_chave = palavra_chave.lower()
		return [
			mentor for mentor in self.obter_mentores_disponiveis()
			if any(palavra_chave in esp.lower() for esp in mentor.especialidades)
		]

	def exibir_diretorio_resumido(self):
		"""Exibe mentores disponíveis com especialidades e contato"""
		mentores_disponiveis = self.obter_mentores_disponiveis()

		print("\n" + "=" * 70)
		print("DIRETORIO DE MENTORES - RF05")
		print("=" * 70)

		if not mentores_disponiveis:
			print("Nenhum mentor disponivel para novas orientacoes no momento.")
			return

		print(f"Mentores disponiveis: {len(mentores_disponiveis)}")
		print("=" * 70)

		for idx, mentor in enumerate(mentores_disponiveis, 1):
			especialidades = ", ".join(mentor.especialidades) if mentor.especialidades else "Nao informadas"
			email = mentor.email if mentor.email else "Nao informado"
			print(f"\n[{idx}] {mentor.nome}")
			print(f"    Departamento: {mentor.departamento}")
			print(f"    Disponibilidade: {mentor.disponibilidade}")
			print(f"    Especialidades: {especialidades}")
			print(f"    Contato: {email}")

	def exibir_contato_mentor(self):
		"""Mostra detalhes de contato e especialidades de um mentor disponível"""
		mentores_disponiveis = self.obter_mentores_disponiveis()
		if not mentores_disponiveis:
			print("\nNenhum mentor disponivel para contato no momento.")
			return

		self.exibir_diretorio_resumido()
		try:
			opcao = int(input("\nDigite o numero do mentor para ver contato (0 para voltar): ").strip())
		except ValueError:
			print("Entrada invalida.")
			return

		if opcao == 0:
			return

		idx = opcao - 1
		if not (0 <= idx < len(mentores_disponiveis)):
			print("Numero invalido.")
			return

		mentor = mentores_disponiveis[idx]
		especialidades = ", ".join(mentor.especialidades) if mentor.especialidades else "Nao informadas"
		linhas = ", ".join(mentor.linhas_pesquisa) if mentor.linhas_pesquisa else "Nao informadas"

		print("\n" + "=" * 70)
		print(f"DETALHES DO MENTOR: {mentor.nome}")
		print("=" * 70)
		print(f"Departamento: {mentor.departamento}")
		print(f"Linhas de pesquisa: {linhas}")
		print(f"Especialidades tecnicas: {especialidades}")
		print(f"Disponibilidade: {mentor.disponibilidade}")
		print(f"Email para contato: {mentor.email if mentor.email else 'Nao informado'}")
		print("=" * 70)




# ===== Persistência de Dados Local (JSON) =====
import json
import os

ARQ_ALUNOS = 'alunos.json'
ARQ_MENTORES = 'mentores.json'
ARQ_PROJETOS = 'projetos.json'

def carregar_dados():
	alunos, mentores, projetos = [], [], []
	# Carregar alunos
	if os.path.exists(ARQ_ALUNOS):
		with open(ARQ_ALUNOS, 'r', encoding='utf-8') as f:
			alunos_data = json.load(f)
			alunos = [Aluno(a['nome'], a['curso'], a['areas_interesse'], a.get('habilidades_tecnicas', [])) for a in alunos_data]
	# Carregar mentores
	if os.path.exists(ARQ_MENTORES):
		with open(ARQ_MENTORES, 'r', encoding='utf-8') as f:
			mentores_data = json.load(f)
			mentores = [Mentor(m['nome'], m['departamento'], m['linhas_pesquisa'], m['disponibilidade'], m.get('email'), m.get('especialidades', [])) for m in mentores_data]
	# Carregar projetos
	if os.path.exists(ARQ_PROJETOS):
		with open(ARQ_PROJETOS, 'r', encoding='utf-8') as f:
			projetos_data = json.load(f)
			# Mapear criadores e participantes por nome
			nome_aluno = {a.nome: a for a in alunos}
			nome_mentor = {m.nome: m for m in mentores}
			for p in projetos_data:
				if p['criador_tipo'] == 'Mentor':
					criador = nome_mentor.get(p['criador_nome'])
				else:
					criador = nome_aluno.get(p['criador_nome'])
				projeto = Projeto(p['titulo'], p['resumo_tema'], p['numero_vagas'], criador)
				projeto.status = p.get('status', 'Em Formação')
				projeto.data_criacao = p.get('data_criacao')
				projeto.participantes = [nome_aluno[n] for n in p.get('participantes', []) if n in nome_aluno]
				projeto.interessados = [nome_aluno[n] for n in p.get('interessados', []) if n in nome_aluno]
				projetos.append(projeto)
	# Atualizar alunos_orientando dos mentores
	if os.path.exists(ARQ_MENTORES):
		with open(ARQ_MENTORES, 'r', encoding='utf-8') as f:
			mentores_data = json.load(f)
			nome_aluno = {a.nome: a for a in alunos}
			for m, mdata in zip(mentores, mentores_data):
				m.alunos_orientando = [nome_aluno[n] for n in mdata.get('alunos_orientando', []) if n in nome_aluno]
	return alunos, mentores, projetos

def salvar_dados(alunos, mentores, projetos):
	with open(ARQ_ALUNOS, 'w', encoding='utf-8') as f:
		json.dump([{
			'nome': a.nome,
			'curso': a.curso,
			'areas_interesse': a.areas_interesse,
			'habilidades_tecnicas': a.habilidades_tecnicas
		} for a in alunos], f, ensure_ascii=False, indent=2)

	with open(ARQ_MENTORES, 'w', encoding='utf-8') as f:
		json.dump([{
			'nome': m.nome,
			'departamento': m.departamento,
			'linhas_pesquisa': m.linhas_pesquisa,
			'disponibilidade': m.disponibilidade,
			'email': m.email,
			'especialidades': m.especialidades,
			'alunos_orientando': [a.nome for a in m.alunos_orientando]
		} for m in mentores], f, ensure_ascii=False, indent=2)

	with open(ARQ_PROJETOS, 'w', encoding='utf-8') as f:
		json.dump([{
			'titulo': p.titulo,
			'resumo_tema': p.resumo_tema,
			'numero_vagas': p.numero_vagas,
			'criador_tipo': 'Mentor' if isinstance(p.criador, Mentor) else 'Aluno',
			'criador_nome': p.criador.nome,
			'participantes': [a.nome for a in p.participantes],
			'status': p.status,
			'data_criacao': p.data_criacao,
			'interessados': [a.nome for a in p.interessados]
		} for p in projetos], f, ensure_ascii=False, indent=2)


# Carregar dados persistentes
alunos, mentores, projetos = carregar_dados()

# Instância do Mural de Projetos - RF04
mural = MuralDeProjetos()
mural.definir_projetos(projetos)

# Instância do Diretório de Mentores - RF05
diretorio_mentores = DiretorioMentores()
diretorio_mentores.definir_mentores(mentores)


# Função para cadastrar um novo aluno
def cadastrar_aluno():
	print("\n=== Cadastro de Aluno ===")
	nome = input("Nome: ")
	curso = input("Curso: ")
	areas = input("Áreas de interesse (separadas por vírgula): ")
	areas_interesse = [a.strip() for a in areas.split(',') if a.strip()]
    
	habilidades = input("Habilidades técnicas/Stacks (separadas por vírgula): ")
	habilidades_tecnicas = [h.strip() for h in habilidades.split(',') if h.strip()]
    
	aluno = Aluno(nome, curso, areas_interesse, habilidades_tecnicas)
	alunos.append(aluno)
	salvar_dados(alunos, mentores, projetos)
	print(f"✓ Aluno cadastrado com sucesso: {aluno.nome}")


# Função para cadastrar um novo mentor - RF02
def cadastrar_mentor():
	print("\n=== Cadastro de Mentor (Professor) - RF02 ===")
	nome = input("Nome completo: ")
	departamento = input("Departamento: ")
    
	linhas = input("Linhas de pesquisa (separadas por vírgula): ")
	linhas_pesquisa = [l.strip() for l in linhas.split(',') if l.strip()]
    
	print("Indique sua disponibilidade para orientar ICs:")
	print("1. Alta (disponível para múltiplas orientações)")
	print("2. Média (disponível para algumas orientações)")
	print("3. Baixa (disponível para poucas orientações)")
	disponibilidade_escolha = input("Escolha (1/2/3): ").strip()
    
	disponibilidade_map = {'1': 'Alta', '2': 'Média', '3': 'Baixa'}
	disponibilidade = disponibilidade_map.get(disponibilidade_escolha, 'Média')
    
	email = input("Email (opcional): ").strip() or None
    
	especialidades = input("Especialidades técnicas (separadas por vírgula, opcional): ")
	especialidades_lista = [e.strip() for e in especialidades.split(',') if e.strip()]
    
	mentor = Mentor(nome, departamento, linhas_pesquisa, disponibilidade, email, especialidades_lista)
	mentores.append(mentor)
	salvar_dados(alunos, mentores, projetos)
	print(f"✓ Mentor cadastrado com sucesso: {mentor.nome}")
	print(f"  Disponibilidade: {mentor.disponibilidade}")
	print(f"  Linhas de pesquisa: {', '.join(mentor.linhas_pesquisa)}")


# Função para publicar uma oportunidade de IC (criar card de projeto) - RF03
def publicar_projeto():
	print("\n=== Publicação de Oportunidade de IC - RF03 ===")
    
	# Escolher o tipo de criador
	print("Quem está criando o projeto?")
	print("1. Mentor (Professor)")
	print("2. Aluno Proponente")
	tipo_criador = input("Escolha (1/2): ").strip()
    
	criador = None
	if tipo_criador == '1':
		if not mentores:
			print("Nenhum mentor cadastrado. Cadastre um mentor primeiro.")
			return
		listar_mentores()
		try:
			idx = int(input("Digite o número do mentor criador: ")) - 1
			if 0 <= idx < len(mentores):
				criador = mentores[idx]
			else:
				print("Número inválido.")
				return
		except ValueError:
			print("Entrada inválida.")
			return
	elif tipo_criador == '2':
		if not alunos:
			print("Nenhum aluno cadastrado. Cadastre um aluno primeiro.")
			return
		listar_alunos()
		try:
			idx = int(input("Digite o número do aluno proponente: ")) - 1
			if 0 <= idx < len(alunos):
				criador = alunos[idx]
			else:
				print("Número inválido.")
				return
		except ValueError:
			print("Entrada inválida.")
			return
	else:
		print("Opção inválida.")
		return
    
	# Coletar informações do projeto
	titulo = input("Título do projeto: ").strip()
	if not titulo:
		print("Título é obrigatório.")
		return
    
	resumo_tema = input("Resumo do tema: ").strip()
	if not resumo_tema:
		print("Resumo é obrigatório.")
		return
    
	try:
		numero_vagas = int(input("Número de vagas para o grupo: ").strip())
		if numero_vagas <= 0:
			print("Número de vagas deve ser positivo.")
			return
	except ValueError:
		print("Número de vagas deve ser um inteiro.")
		return
    
	# Criar o projeto
	projeto = Projeto(titulo, resumo_tema, numero_vagas, criador)
	projetos.append(projeto)
	salvar_dados(alunos, mentores, projetos)
	print(f"✓ Projeto publicado com sucesso: '{projeto.titulo}'")
	print(f"  Criado por: {criador.nome} ({'Mentor' if isinstance(criador, Mentor) else 'Aluno'})")
	print(f"  Vagas: {projeto.numero_vagas}")


# Função para listar todos os mentores
def listar_mentores():
	print("\n=== Lista de Mentores Cadastrados ===")
	if not mentores:
		print("Nenhum mentor cadastrado ainda.")
		return
	
	for idx, mentor in enumerate(mentores, 1):
		print(f"\n{idx}. {mentor.nome}")
		print(f"   Departamento: {mentor.departamento}")
		print(f"   Linhas de pesquisa: {', '.join(mentor.linhas_pesquisa)}")
		print(f"   Disponibilidade: {mentor.disponibilidade}")
		if mentor.email:
			print(f"   Email: {mentor.email}")
		if mentor.especialidades:
			print(f"   Especialidades técnicas: {', '.join(mentor.especialidades)}")
		print(f"   Alunos orientando: {len(mentor.alunos_orientando)}")


# Função para listar todos os alunos
def listar_alunos():
	print("\n=== Lista de Alunos Cadastrados ===")
	if not alunos:
		print("Nenhum aluno cadastrado ainda.")
		return
	
	for idx, aluno in enumerate(alunos, 1):
		print(f"\n{idx}. {aluno.nome}")
		print(f"   Curso: {aluno.curso}")
		print(f"   Áreas de interesse: {', '.join(aluno.areas_interesse)}")
		print(f"   Habilidades técnicas: {', '.join(aluno.habilidades_tecnicas)}")


# Função para listar todos os projetos
def listar_projetos():
	print("\n=== Lista de Projetos Publicados ===")
	if not projetos:
		print("Nenhum projeto publicado ainda.")
		return
	
	for idx, projeto in enumerate(projetos, 1):
		tipo_criador = "Mentor" if isinstance(projeto.criador, Mentor) else "Aluno"
		print(f"\n{idx}. {projeto.titulo}")
		print(f"   Criado por: {projeto.criador.nome} ({tipo_criador})")
		print(f"   Resumo: {projeto.resumo_tema}")
		print(f"   Vagas: {projeto.numero_vagas}")
		print(f"   Participantes: {len(projeto.participantes)}")
		print(f"   Status: {projeto.status}")


def alterar_status_vaga():
	"""RF08 - Permite ao responsável marcar status do projeto"""
	if not projetos:
		print("\nNenhum projeto cadastrado ainda.")
		return
	
	print("\n=== Alterar Status da Vaga (RF08) ===")
	for idx, projeto in enumerate(projetos, 1):
		print(f"{idx}. {projeto.titulo} - Status atual: {projeto.status}")

	try:
		idx = int(input("Escolha o número do projeto para atualizar (0 para voltar): ").strip()) - 1
		if idx == -1:
			return
		if not (0 <= idx < len(projetos)):
			print("Número inválido.")
			return
	except ValueError:
		print("Entrada inválida.")
		return
	
	projeto = projetos[idx]

	print("\nSelecione o novo status:")
	print("1. Em Formação (vagas abertas)")
	print("2. Grupo Fechado (IC iniciada)")
	status_choice = input("Escolha (1/2): ").strip()

	if status_choice == '1':
		projeto.marcar_em_formacao()
		print(f"Status atualizado para 'Em Formação' em '{projeto.titulo}'")
	elif status_choice == '2':
		projeto.marcar_grupo_fechado()
		print(f"Status atualizado para 'Grupo Fechado' em '{projeto.titulo}'")
	else:
		print("Opção inválida. Nenhuma alteração feita.")


# Função para exibir o Mural de Projetos - RF04
def exibir_mural_projetos():
	"""Exibe o mural de projetos com opções de visualização"""
	while True:
		print("\n" + "="*70)
		print("MURAL DE PROJETOS - RF04")
		print("="*70)
		print("1. Visualizar todos os projetos abertos (Resumido)")
		print("2. Visualizar detalhes completos dos projetos")
		print("3. Buscar projetos por tema/palavra-chave")
		print("4. Filtrar projetos por tipo de criador (Mentor/Aluno)")
		print("5. Estatísticas do mural")
		print("6. Voltar ao menu principal")
		print("="*70)
		
		opcao = input("Escolha uma opção (1-6): ").strip()
		
		if opcao == '1':
			mural.exibir_mural_resumido()
		
		elif opcao == '2':
			mural.exibir_mural_detalhado()
		
		elif opcao == '3':
			palavra_chave = input("\nDigite a palavra-chave para buscar: ").strip()
			if palavra_chave:
				mural.exibir_mural_com_filtro(palavra_chave)
			else:
				print("Palavra-chave vazia. Tente novamente.")
		
		elif opcao == '4':
			print("\nFiltrar por tipo de criador:")
			print("1. Projetos de Mentores")
			print("2. Projetos de Alunos")
			tipo_escolha = input("Escolha (1/2): ").strip()
			
			if tipo_escolha == '1':
				projetos_filtrados = mural.filtrar_por_criador_tipo('Mentor')
				tipo_nome = "Mentores"
			elif tipo_escolha == '2':
				projetos_filtrados = mural.filtrar_por_criador_tipo('Aluno')
				tipo_nome = "Alunos"
			else:
				print("Opção inválida.")
				continue
			
			if not projetos_filtrados:
				print(f"\nNenhum projeto de {tipo_nome} disponível.")
			else:
				print(f"\n{'='*70}")
				print(f"PROJETOS DE {tipo_nome.upper()}")
				print(f"Total: {len(projetos_filtrados)} projeto(s)")
				print(f"{'='*70}")
				
				for idx, projeto in enumerate(projetos_filtrados, 1):
					print(f"\n[{idx}] {projeto.titulo}")
					print(f"    Criador: {projeto.criador.nome}")
					print(f"    Tema: {projeto.resumo_tema}")
					print(f"    Vagas disponíveis: {projeto.vagas_disponiveis()} de {projeto.numero_vagas}")
		
		elif opcao == '5':
			projetos_abertos = mural.obter_projetos_em_formacao()
			projetos_com_vagas = mural.obter_projetos_com_vagas()
			
			print("\n" + "="*70)
			print("ESTATÍSTICAS DO MURAL DE PROJETOS")
			print("="*70)
			print(f"Total de projetos publicados: {len(projetos)}")
			print(f"Total de projetos em formação: {len(projetos_abertos)}")
			print(f"Projetos com vagas livres:    {len(projetos_com_vagas)}")
			print(f"Total de vagas disponíveis:   {mural.contar_vagas_totais_disponiveis()}")
			
			if projetos:
				projeto_mais_concorrido = max(projetos, key=lambda p: len(p.participantes))
				print(f"\nProjeto mais concorrido:       '{projeto_mais_concorrido.titulo}' ({len(projeto_mais_concorrido.participantes)} participantes)")
			
			if projetos_abertos:
				projeto_vazio = max(projetos_abertos, key=lambda p: p.vagas_disponiveis())
				print(f"Projeto com mais vagas:        '{projeto_vazio.titulo}' ({projeto_vazio.vagas_disponiveis()} vagas livres)")
			
			print("="*70)
		
		elif opcao == '6':
			break
		
		else:
			print("Opção inválida. Tente novamente.")


# Função para visualizar detalhes de um mentor
def visualizar_mentor():
	listar_mentores()
	if mentores:
		try:
			idx = int(input("\nDigite o número do mentor para ver detalhes (ou 0 para voltar): ")) - 1
			if 0 <= idx < len(mentores):
				mentor = mentores[idx]
				print(f"\n=== Detalhes do Mentor: {mentor.nome} ===")
				print(f"Departamento: {mentor.departamento}")
				print(f"Linhas de pesquisa: {', '.join(mentor.linhas_pesquisa)}")
				print(f"Disponibilidade para orientações: {mentor.disponibilidade}")
				if mentor.email:
					print(f"Email: {mentor.email}")
				if mentor.especialidades:
					print(f"Especialidades técnicas: {', '.join(mentor.especialidades)}")
				print(f"Total de alunos orientando: {len(mentor.alunos_orientando)}")
				if mentor.alunos_orientando:
					print("Alunos:")
					for aluno in mentor.alunos_orientando:
						print(f"  - {aluno.nome}")
		except ValueError:
			print("Opção inválida.")


# Função para exibir o Diretório de Mentores - RF05
def exibir_diretorio_mentores():
	"""Exibe o diretório de mentores disponíveis para contato"""
	while True:
		print("\n" + "=" * 70)
		print("DIRETORIO DE MENTORES - RF05")
		print("=" * 70)
		print("1. Listar mentores disponiveis")
		print("2. Buscar mentores por especialidade")
		print("3. Ver detalhes de contato de um mentor")
		print("4. Voltar ao menu principal")
		print("=" * 70)

		opcao = input("Escolha uma opcao (1-4): ").strip()

		if opcao == '1':
			diretorio_mentores.exibir_diretorio_resumido()

		elif opcao == '2':
			palavra_chave = input("\nDigite a especialidade para buscar: ").strip()
			if not palavra_chave:
				print("Especialidade vazia. Tente novamente.")
				continue

			mentores_filtrados = diretorio_mentores.filtrar_por_especialidade(palavra_chave)
			print("\n" + "=" * 70)
			print(f"RESULTADOS DA BUSCA - ESPECIALIDADE: {palavra_chave}")
			print("=" * 70)
			if not mentores_filtrados:
				print("Nenhum mentor disponivel com essa especialidade.")
			else:
				for idx, mentor in enumerate(mentores_filtrados, 1):
					especialidades = ", ".join(mentor.especialidades) if mentor.especialidades else "Nao informadas"
					email = mentor.email if mentor.email else "Nao informado"
					print(f"\n[{idx}] {mentor.nome}")
					print(f"    Departamento: {mentor.departamento}")
					print(f"    Disponibilidade: {mentor.disponibilidade}")
					print(f"    Especialidades: {especialidades}")
					print(f"    Contato: {email}")

		elif opcao == '3':
			diretorio_mentores.exibir_contato_mentor()

		elif opcao == '4':
			break

		else:
			print("Opcao invalida. Tente novamente.")


# Função para manifestar interesse em um projeto - RF06
def manifestar_interesse():
	print("\n=== Manifestar Interesse em Projeto - RF06 ===")
	
	if not alunos:
		print("Nenhum aluno cadastrado. Cadastre um aluno primeiro.")
		return
	
	if not mural.obter_projetos_com_vagas():
		print("Nenhum projeto com vagas disponíveis no momento.")
		return
	
	# Escolher aluno interessado
	listar_alunos()
	try:
		idx_aluno = int(input("Digite o número do aluno interessado: ")) - 1
		if not (0 <= idx_aluno < len(alunos)):
			print("Número inválido.")
			return
		aluno = alunos[idx_aluno]
	except ValueError:
		print("Entrada inválida.")
		return
	
	# Listar projetos com vagas
	projetos_com_vagas = mural.obter_projetos_com_vagas()
	print("\nProjetos com vagas disponíveis:")
	for idx, projeto in enumerate(projetos_com_vagas, 1):
		tipo_criador = "Mentor" if isinstance(projeto.criador, Mentor) else "Aluno"
		print(f"{idx}. {projeto.titulo}")
		print(f"   Tema: {projeto.resumo_tema}")
		print(f"   Criador: {projeto.criador.nome} ({tipo_criador})")
		print(f"   Vagas disponíveis: {projeto.vagas_disponiveis()} de {projeto.numero_vagas}")
		print(f"   Participantes atuais: {len(projeto.participantes)}")
		if projeto.interessados:
			print(f"   Alunos interessados: {len(projeto.interessados)}")
		print()
	
	try:
		idx_projeto = int(input("Digite o número do projeto de interesse: ")) - 1
		if not (0 <= idx_projeto < len(projetos_com_vagas)):
			print("Número inválido.")
			return
		projeto = projetos_com_vagas[idx_projeto]
	except ValueError:
		print("Entrada inválida.")
		return
	
	# Adicionar interesse
	if projeto.adicionar_interessado(aluno):
		print(f"\n✓ Interesse manifestado com sucesso!")
		print(f"  Aluno: {aluno.nome}")
		print(f"  Projeto: {projeto.titulo}")
		print(f"  Responsável notificado: {projeto.criador.nome}")
		
	else:
		print("Você já manifestou interesse neste projeto.")


# Função para visualizar interessados nos projetos - RF07
def visualizar_interessados():
	print("\n=== Visualizar Interessados nos Projetos - RF07 ===")
	
	if not projetos:
		print("Nenhum projeto publicado ainda.")
		return
	
	# Escolher tipo de criador
	print("Quem está visualizando os interessados?")
	print("1. Mentor (Professor)")
	print("2. Aluno Proponente")
	tipo_criador = input("Escolha (1/2): ").strip()
	
	criadores = []
	if tipo_criador == '1':
		if not mentores:
			print("Nenhum mentor cadastrado.")
			return
		criadores = mentores
		tipo_nome = "Mentor"
	elif tipo_criador == '2':
		if not alunos:
			print("Nenhum aluno cadastrado.")
			return
		criadores = alunos
		tipo_nome = "Aluno"
	else:
		print("Opção inválida.")
		return
	
	# Listar criadores
	print(f"\n{tipo_nome}s disponíveis:")
	for idx, criador in enumerate(criadores, 1):
		print(f"{idx}. {criador.nome}")
	
	try:
		idx_criador = int(input(f"Digite o número do {tipo_nome.lower()}: ")) - 1
		if not (0 <= idx_criador < len(criadores)):
			print("Número inválido.")
			return
		criador = criadores[idx_criador]
	except ValueError:
		print("Entrada inválida.")
		return
	
	# Listar projetos do criador
	projetos_criador = [p for p in projetos if p.criador == criador]
	if not projetos_criador:
		print(f"Nenhum projeto criado por {criador.nome}.")
		return
	
	print(f"\nProjetos criados por {criador.nome}:")
	for idx, projeto in enumerate(projetos_criador, 1):
		print(f"{idx}. {projeto.titulo} - Status: {projeto.status} - Interessados: {len(projeto.interessados)}")
	
	try:
		idx_projeto = int(input("Digite o número do projeto: ")) - 1
		if not (0 <= idx_projeto < len(projetos_criador)):
			print("Número inválido.")
			return
		projeto = projetos_criador[idx_projeto]
	except ValueError:
		print("Entrada inválida.")
		return
	
	# Mostrar interessados
	if not projeto.interessados:
		print(f"\nNenhum aluno manifestou interesse em '{projeto.titulo}' ainda.")
		return
	
	print(f"\n{'='*70}")
	print(f"ALUNOS INTERESSADOS EM: {projeto.titulo}")
	print(f"Total: {len(projeto.interessados)} aluno(s)")
	print(f"{'='*70}")
	
	for idx, aluno in enumerate(projeto.interessados, 1):
		print(f"\n--- Aluno #{idx}: {aluno.nome} ---")
		print(f"Curso: {aluno.curso}")
		print(f"Áreas de interesse: {', '.join(aluno.areas_interesse)}")
		print(f"Habilidades técnicas: {', '.join(aluno.habilidades_tecnicas)}")
		print("---")
	
	print(f"\n{'='*70}")


# Menu principal
def menu_principal():
	while True:
		print("\n" + "="*50)
		print("FIAP Skill-Match - O Tinder de Projetos IC")
		print("="*50)
		print("1. Cadastrar Aluno")
		print("2. Cadastrar Mentor (Professor) - RF02")
		print("3. Listar Alunos")
		print("4. Listar Mentores")
		print("5. Visualizar Detalhes de Mentor")
		print("6. Publicar Projeto - RF03")
		print("7. Mural de Projetos - RF04")
		print("8. Diretorio de Mentores - RF05")
		print("9. Manifestar Interesse em Projeto - RF06")
		print("10. Visualizar Interessados nos Projetos - RF07")
		print("11. Gerenciar Status da Vaga - RF08")
		print("12. Sair")
		print("="*50)
		
		opcao = input("Escolha uma opcao (1-11): ").strip()
		
		if opcao == '1':
			cadastrar_aluno()
		elif opcao == '2':
			cadastrar_mentor()
		elif opcao == '3':
			listar_alunos()
		elif opcao == '4':
			listar_mentores()
		elif opcao == '5':
			visualizar_mentor()
		elif opcao == '6':
			publicar_projeto()
		elif opcao == '7':
			exibir_mural_projetos()
		elif opcao == '8':
			exibir_diretorio_mentores()
		elif opcao == '9':
			manifestar_interesse()
		elif opcao == '10':
			visualizar_interessados()
		elif opcao == '11':
			alterar_status_vaga()
		elif opcao == '12':
			print("\nAté logo! Sistema finalizado.")
			break
		else:
			print("Opcao invalida. Tente novamente.")


# Exemplo de uso
if __name__ == "__main__":
	menu_principal()
