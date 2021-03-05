'''
Sistema de Cadastro de Pessoa com possibilidade de Incluir/Editar/Visualizar/Deletar (CRUD)
Python-Flask utilizando o banco de dados SQLite
Front-end: HTML/CSS
Desenvolvido por Beatriz Ambrosio, Matheus Germano Dos Santos e Renato Uccella.
'''

# Import do Flask e da extensão flask-sqlalchemy.
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

# Configuração do sqlalchemy indicando o caminho do banco de dados a ser criado.
app = Flask(__name__) # , static_url_path='/static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# Modelagem da Tabela Persons.
class Persons(db.Model):
   id = db.Column('person_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   email = db.Column(db.String(100))
   phone = db.Column(db.String(22))
   birth = db.Column(db.String(10))

   def __init__(self, name, email, phone, birth):
      self.name = name
      self.email = email
      self.phone = phone
      self.birth = birth

# Definição de rotas.

# Página Inicial
@app.route('/')
def home():
   return render_template('home.html', title='Home')


# Listar todas as pessoas
@app.route('/show_all')
def show_all():
   return render_template('show_all.html', persons=Persons.query.all(), title='Lista')


# Inclusão de pessoas.
@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      # Caso um campo esteja vazio, retorna erro. Caso contrário, adiciona a pessoa.
      if not request.form['name'] or not request.form['email'] or not request.form['phone'] or not request.form['birth']:
         flash('Por favor, preencha todos os campos!', 'error')
      else:
         pessoa = Persons(request.form['name'], request.form['email'], request.form['phone'], request.form['birth'])
         db.session.add(pessoa)
         db.session.commit()
         flash(f'{pessoa.name} cadastrado(a) com sucesso!')  # mostra mensagem pro usuário
         return redirect(url_for('show_all'))
   return render_template('new.html', title='Cadastro')


# Deletar Pessoas. Recebe id da pessoa como parâmetro.
@app.route('/delete/<int:person_id>', methods = ['POST'])
def delete(person_id):
   person = Persons.query.get(person_id) 
   if person:
      nome_excluido = person.name
      db.session.delete(person)
      db.session.commit()
      flash(f'{nome_excluido} foi excluído(a)!')
   return redirect(url_for('show_all'))


# Atualização de cadastro. Recebe id da pessoa como parâmetro.
@app.route('/edit/<int:person_id>', methods = ['GET', 'POST'])
def edit(person_id):
   person = Persons.query.get(person_id)
   if request.method == 'POST':
      if not request.form['name'] or not request.form['email'] or not request.form['phone'] or not request.form['birth']:
         flash('Por favor, preencha todos os campos!', 'error')
      else:
         person.name = request.form['name']
         person.email = request.form['email']
         person.phone = request.form['phone']
         person.birth = request.form['birth']
         db.session.commit()
         flash('Alteração realizada com sucesso!')  # mostra mensagem para o usuário.
         return redirect(url_for('show_all'))
   # O template recebe os dados da pessoa para pré-preencher o formulário.
   return render_template('edit.html', title='Edição', person=person)


# Créditos.
@app.route('/creditos')
def creditos():
   return render_template('creditos.html', title='Créditos')


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)