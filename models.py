from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import  declarative_base

engine = create_engine('sqlite:///atividades.db', convert_unicode=True)
#atividades.db é o nome dado ao banco de dados
#convert unicode= true é para não ter problemas com acentuação
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
#autocommit é parâmetro de sessiomaker e sessionmaker é parâmetro de scoped_session
#tem que passar a engine para saber qual o banco que tem que abrir a sessão
Base = declarative_base()
Base.query = db_session.query_property()
#esse trecho é o necessário para criar o banco de dados e fazer as consultas

class Pessoas(Base):
    __tablename__='pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), index=True)
    idade = Column(Integer)

#quando mandar imprimir objeto ele vai mandar o que tem nessa função. repr = representação da classe
    def __repr__(self):
        return '<Pessoa {}>'.format(self.nome) #vai imprimir a pessoa e o nome da pessoa

    #com esse método pode retirar do arquivo utils o db_session do import. Pq chama o método da própria classe
    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Atividades(Base):
    __tablename__='atividades'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    pessoa_id = Column(Integer, ForeignKey('pessoas.id')) #aqui não é o nome da classe, é o nome da tabela, por isso é pessoas e não Pessoas
    pessoa = relationship("Pessoas") #classe Pessoas. Vai reconhecer que tem relacionamento de atividades com pessoas

def init_db():
    Base.metadata.create_all(bind=engine) #esse comando create_all que vai criar o banco de dados

#o main é para que ninguém consiga chamar o arquivo de fora e sair criando banco e tabela
#quando da o run 'models' ele cria um arquivo chamado atividades.db, que é o banco de dados propriamente dito
if __name__ == '__main__':
    init_db()