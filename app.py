from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# criar banco de dados
db_name = 'meus_dados.db'

# função para criar tabela
def init_db():
    connect = sqlite3.connect(db_name)
    c = connect.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS pessoa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            curso TEXT NOT NULL
        )
        '''
    )
    connect.commit()
    connect.close()

# inicializar o database na primeira execução
init_db()

# Criar uma rota para o index.html funcionar

@app.route('/')
def home():
    return render_template('index.html')

# Criar uma rota para o resposta.html funcionar


@app.route("/resposta", methods=["POST"])
def resposta(): 
    curso = request.form['curso']
    connect = sqlite3.connect(db_name)
    c = connect.cursor()
    c.execute("INSERT INTO pessoa (curso) VALUES (?)", (curso,))
    connect.commit()
    connect.close()
    return render_template('resposta.html', curso=curso)


@app.route('/lista')
def lista():
    connect = sqlite3.connect(db_name)
    c = connect.cursor()
    c.execute("SELECT id, curso FROM pessoa")
    cursos = c.fetchall()
    connect.close()
    return render_template('lista.html', cursos=cursos)


@app.route('/deletar/<int:id>')
def deletar(id):
    connect = sqlite3.connect(db_name)
    c = connect.cursor()
    c.execute("DELETE FROM pessoa WHERE id = ?", (id,))
    connect.commit()
    connect.close()
    return redirect(url_for('lista'))

if __name__ == '__main__':
    app.run(debug=True)