
# Classe para representar um aluno
class Aluno:
	def __init__(self, nome, curso, areas_interesse):
		self.nome = nome
		self.curso = curso
		self.areas_interesse = areas_interesse  # lista de strings

	def __repr__(self):
		return f"Aluno(nome={self.nome}, curso={self.curso}, areas_interesse={self.areas_interesse})"

# Lista para armazenar os alunos cadastrados
alunos = []

# Função para cadastrar um novo aluno
def cadastrar_aluno():
	print("=== Cadastro de Aluno ===")
	nome = input("Nome: ")
	curso = input("Curso: ")
	areas = input("Áreas de interesse (separadas por vírgula): ")
	areas_interesse = [a.strip() for a in areas.split(',') if a.strip()]
	aluno = Aluno(nome, curso, areas_interesse)
	alunos.append(aluno)
	print(f"Aluno cadastrado: {aluno}")

# Exemplo de uso
if __name__ == "__main__":
	cadastrar_aluno()
