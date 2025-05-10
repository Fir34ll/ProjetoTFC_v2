from flask import Flask, render_template, redirect, url_for, session
from rotas.rotalogin import rotalogin
from rotas.rotaindex import rotaindex
from rotas.rotagraficos import rotagraficos
from rotas.rotaperfil import rotaperfil
from rotas.rotaflls import rotaflls
from rotas.rotaaçoes import rotaaçoes
from rotas.rotacarteira import rotacarteira
from rotas.rotarecomendacao import rotarecomendacao

app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.route('/')
def first():
    return render_template('first.html')

@app.route('/elements')
def elements():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('elements.html')

@app.route('/iniciante')
def iniciante():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('iniciante.html')

@app.route('/intermediario')
def intermediario():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('intermediario.html')

@app.route('/avançado')
def avançado():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('avançado.html')

@app.route('/emocional')
def emocional():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('emocional.html')

@app.route('/gerenciamento')
def gerenciamento():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('gerenciamento.html')

@app.route('/indexcalculadora')
def indexcalculadora():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('indexcalculadora.html')

@app.route('/generic')
def generic():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('generic.html')

@app.route('/indeximposto')
def indeximposto():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('indeximposto.html')

@app.route('/indexemprestimos')
def indexemprestimos():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('indexemprestimos.html')

@app.route('/recomendacoes')
def recomendacoes():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('recomendacoes.html')
    
app.register_blueprint(rotalogin)
app.register_blueprint(rotaindex)
app.register_blueprint(rotagraficos)
app.register_blueprint(rotaperfil)
app.register_blueprint(rotaflls)
app.register_blueprint(rotaaçoes)
app.register_blueprint(rotacarteira)
app.register_blueprint(rotarecomendacao)

if __name__ == '__main__':
    app.run(debug=True)
