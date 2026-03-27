
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
	
	def __repr__(self):
		tipo_criador = "Mentor" if isinstance(self.criador, Mentor) else "Aluno"
		return f"Projeto(titulo={self.titulo}, resumo={self.resumo_tema[:50]}..., vagas={self.numero_vagas}, criador={tipo_criador} {self.criador.nome})"


# Listas para armazenar os usuários cadastrados
alunos = []
mentores = []
projetos = []


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
		print("7. Listar Projetos")
		print("8. Sair")
		print("="*50)
		
		opcao = input("Escolha uma opção (1-8): ").strip()
		
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
			listar_projetos()
		elif opcao == '8':
			print("\nAté logo! Sistema finalizado.")
			break
		else:
			print("Opção inválida. Tente novamente.")


# Exemplo de uso
if __name__ == "__main__":
	menu_principal()
