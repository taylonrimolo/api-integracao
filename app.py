from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# nome do banco de dados
db_name = 'meus_dados.db'

# função para criar tabelas
def init_db():
    connect = sqlite3.connect(db_name)
    c = connect.cursor()
    # tabela de cursos
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS pessoa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            curso TEXT NOT NULL
        )
        '''
    )
    # tabela de estudantes
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            curso_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            FOREIGN KEY (curso_id) REFERENCES pessoa (id)
        )
        '''
    )
    connect.commit()
    connect.close()

# inicializar banco de dados
init_db()

# rota inicial
@app.route('/')
def home():
    return render_template('index.html')

# rota para salvar curso
@app.route("/resposta", methods=["POST"])
def resposta(): 
    curso = request.form['curso']
    connect = sqlite3.connect(db_name)
    c = connect.cursor()
    c.execute("INSERT INTO pessoa (curso) VALUES (?)", (curso,))
    connect.commit()
    connect.close()
    return render_template('resposta.html', curso=curso)

# rota para listar cursos
@app.route('/lista')
def lista():
    connect = sqlite3.connect(db_name)
    c = connect.cursor()
    c.execute("SELECT id, curso FROM pessoa")
    cursos = c.fetchall()
    connect.close()
    return render_template('lista.html', cursos=cursos)

# rota para deletar curso
@app.route('/deletar/<int:id>')
def deletar(id):
    connect = sqlite3.connect(db_name)
    c = connect.cursor()
    c.execute("DELETE FROM pessoa WHERE id = ?", (id,))
    connect.commit()
    connect.close()
    return redirect(url_for('lista'))

# rota para cadastrar quantidade de estudantes
@app.route('/estudantes', methods=['GET', 'POST'])
def estudantes():
    connect = sqlite3.connect(db_name)
    c = connect.cursor()

    if request.method == 'POST':
        curso_id = request.form['curso_id']
        quantidade = request.form['quantidade']
        c.execute("INSERT INTO estudantes (curso_id, quantidade) VALUES (?, ?)",
                  (curso_id, quantidade))
        connect.commit()
    
    c.execute("SELECT id, curso FROM pessoa")
    cursos = c.fetchall()
    connect.close()
    return render_template('estudantes.html', cursos=cursos)

# rota para listar cursos com quantidade de alunos
@app.route('/lista_alunos')
def lista_alunos():
    connect = sqlite3.connect(db_name)
    c = connect.cursor()
    c.execute('''
        SELECT pessoa.curso, estudantes.quantidade
        FROM estudantes
        JOIN pessoa ON estudantes.curso_id = pessoa.id
    ''')
    dados = c.fetchall()
    connect.close()
    return render_template('lista_alunos.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)