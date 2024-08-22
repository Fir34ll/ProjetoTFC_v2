import pyrebase
from firebase_admin import auth, db
from flask import Blueprint, render_template, redirect, url_for, session
from rotas.config import config
rotaindex = Blueprint('rotaindex', __name__)


# Configuração do Firebase

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Rotas da pagina index
@rotaindex.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))

    user_id = session['user']
    
    try:
        user_info = auth.get_account_info(user_id)
        firebase_user_id = user_info['users'][0]['localId']
        
        user_info_ref = db.child("users").child(firebase_user_id).child("info")
        user_info_data = user_info_ref.get().val()
        
        if not user_info_data:
            print("Nenhum dado encontrado para o usuário.")
            return redirect(url_for('login'))
        
        name = user_info_data.get('name')
        perfil_investidor = user_info_data.get('perfilinvestidor')

        print(f"Nome do usuário: {name}")
        print(f"Perfil investidor: {perfil_investidor}")

        if name is None:
            return redirect(url_for('login'))
        
    except Exception as e:
        print(f"Erro ao buscar dados do usuário: {e}")
        return redirect(url_for('login'))

    return render_template('index.html', name=name, perfilinvestidor=perfil_investidor)