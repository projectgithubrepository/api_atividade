from models import Pessoas

#insere dados na tabela pessoa
def insere_pessoas():
    pessoa = Pessoas(nome='Daniel',idade=32)
    print(pessoa)
    pessoa.save() #aqui chama o método save da classe Pessoas que está no arquivo models

#realiza consulta na tabela pessoa
def consulta_pessoas():
    pessoas = Pessoas.query.all()
    print(pessoas)
    pessoas = Pessoas.query.filter_by(nome='Daniel').first()
    print(pessoas.idade)

#altera dados na tabela pessoa
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Daniel').first()
    pessoa.nome = 'Mujica'
    pessoa.save()

#exclui dados na tabela pessoa
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Daniel').first()
    pessoa.delete()

if __name__ == '__main__':
    # insere_pessoas()
    # altera_pessoa()
    # exclui_pessoa()
    consulta_pessoas()
