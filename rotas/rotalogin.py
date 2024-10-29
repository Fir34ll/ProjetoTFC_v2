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
            try:
                name = request.form.get('name')
                email = request.form.get('email')
                password = request.form.get('password')
                
                # Tenta criar o usuário
                user = auth.create_user_with_email_and_password(email, password)
                user_id = user['localId']
                
                # Salva as informações adicionais
                db.child("users").child(user_id).child("info").set({"name": name})
                
                flash("Registro realizado com sucesso!", "success")
                return redirect(url_for('rotalogin.login'))
                
            except Exception as e:
                error_message = str(e)
                if "EMAIL_EXISTS" in error_message:
                    flash("Este email já está registrado.", "error")
                elif "WEAK_PASSWORD" in error_message:
                    flash("A senha deve ter pelo menos 6 caracteres.", "error")
                elif "INVALID_EMAIL" in error_message:
                    flash("Email inválido.", "error")
                else:
                    flash("Erro no registro: " + error_message, "error")
                return render_template('login.html')
        else:
            try:
                email = request.form['email']
                password = request.form['password']
                
                user = auth.sign_in_with_email_and_password(email, password)
                session['user'] = user['idToken']
                return redirect(url_for('rotaindex.index'))
                
            except Exception as e:
                error_message = str(e)
                if "INVALID_PASSWORD" in error_message:
                    flash("Senha incorreta.", "error")
                elif "EMAIL_NOT_FOUND" in error_message:
                    flash("Email não encontrado.", "error")
                else:
                    flash("Erro no login: " + error_message, "error")
                return render_template('login.html')

    return render_template('login.html')

    

@rotalogin.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('rotalogin.login'))
