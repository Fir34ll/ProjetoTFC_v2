from flask import render_template, request, redirect, url_for, session
import pyrebase
from flask import Blueprint, render_template, redirect, url_for, session
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

            # Adicione logs para verificar se os dados estão corretos
            print(f"Received registration request. Name: {name}, Email: {email}")

            try:
                # Cria um novo usuário
                user = auth.create_user_with_email_and_password(email, password)
                user_id = user['localId']
                
                # Verifique a criação do usuário e o ID
                print(f"User created with ID: {user_id}")

                # Salvar o nome do usuário no Firebase Realtime Database
                db.child("users").child(user_id).child("info").set({"name": name})
                
                # Verifique se os dados foram salvos corretamente
                saved_data = db.child("users").child(user_id).get().val()
                print(f"Saved data: {saved_data}")

                return "Registration successful. You can now log in."
            except Exception as e:
                print(f"Error during registration: {e}")
                return f"Error during registration: {e}"
        else:
            email = request.form['email']
            password = request.form['password']
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                session['user'] = user['idToken']
                return redirect(url_for('rotaindex.index'))
            except Exception as e:
                print(f"Login failed: {e}")
                return f"Login failed: {e}"
    return render_template('login.html')
    

@rotalogin.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('rotalogin.login'))

