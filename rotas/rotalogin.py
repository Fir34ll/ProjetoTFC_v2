from flask import render_template, request, redirect, url_for, session, flash
import pyrebase
from flask import Blueprint
from rotas.config import config

rotalogin = Blueprint('rotalogin', __name__)

# Configuração do Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@rotalogin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'register':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            try:
                # Cria um novo usuário
                user = auth.create_user_with_email_and_password(email, password)
                user_id = user['localId']

                # Salvar o nome do usuário no Firebase Realtime Database
                db.child("users").child(user_id).child("info").set({"name": name})

                # Mensagem de sucesso
                flash("Registro feito com sucesso. Você pode fazer login agora.", "success")
            except Exception as e:
                # Mensagem de erro
                flash(f"Erro durante o registro: {e}", "error")
            return redirect(url_for('rotalogin.login'))
        else:
            email = request.form['email']
            password = request.form['password']
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                session['user'] = user['idToken']
                return redirect(url_for('rotaindex.index'))
            except Exception as e:
                # Mensagem de erro no login
                flash(f"Login failed: {e}", "error")
            return redirect(url_for('rotalogin.login'))
    return render_template('login.html')

    

@rotalogin.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('rotalogin.login'))

