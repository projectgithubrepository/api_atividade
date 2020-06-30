from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades

app = Flask(__name__)
api = Api(app)

class Pessoa(Resource):
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome':pessoa.nome,
                'idade':pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status':'error',
                'mensagem':'Pessoa não encontrada.'
            }
        return response

    # def post(self, nome):
    #     pessoa = Pessoas.query.filter_by(nome=nome).first()
    #     dados = request.json
    #     #request.data vai ser substituído por request.json, pq não vai usar outro formato. Se usar outro formato vai retornar erro
    #     print(dados)
    #     return {'nome':'Thor'}

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        #request.data vai ser substituído por request.json, pq não vai usar outro formato. Se usar outro formato vai retornar erro
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluída com sucesso.'.format(pessoa.nome)
        pessoa.delete()
        return {'status':'sucesso', 'mensagem':mensagem}

#retorna tudo de um DB. Não é aconselhável fazer sem filtro, por motivo de travar pela quantidade de dados.
class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        #response = [i for i in pessoas] #como é um objeto precisa transformar em lista, por isso essa linha é substituído por
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]
        return response

    def post(self):
        dados = request.json
        #request.data vai ser substituído por request.json, pq não vai usar outro formato. Se usar outro formato vai retornar erro
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        # response = [i for i in pessoas] #como é um objeto precisa transformar em lista, por isso essa linha é substituído por
        response = [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome} for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id
        }
        return response



api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')


if __name__ == '__main__':
    app.run(debug=True)
