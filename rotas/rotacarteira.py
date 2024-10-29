from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests, pyrebase
import time
from rotas.config import config
from flask import Blueprint, render_template, redirect, url_for, session

rotacarteira = Blueprint('rotacarteira', __name__)

# Configuração do Firebase

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@rotacarteira.route('/indexcarteira')
def indexcarteira():
    # Verifica se o usuário está na sessão
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    
    try:
        # Obtém as informações da conta do usuário
        user_id = auth.get_account_info(session['user'])['users'][0]['localId']
        user_data = db.child("users").child(user_id).get().val()
        return render_template('indexcarteira.html', user_data=user_data)
    except requests.exceptions.HTTPError as e:
        # Verifica se o erro é um token inválido
        if hasattr(e, 'response') and e.response is not None:
            response = e.response
            if response.status_code == 400 and 'INVALID_ID_TOKEN' in response.text:
                # Redireciona para a página de login se o token for inválido
                return redirect(url_for('rotalogin.login'))
        # Para outros erros HTTP, re-levanta a exceção
        raise

# Rotas da API

@rotacarteira.route('/get_quote', methods=['POST'])
def get_quote():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    symbol = request.form['symbol']
    token = 'xoAToPKAai8jfSwukJspez'  
    url = f'https://brapi.dev/api/quote/{symbol}?token={token}'
    try:
        print("API Request URL:", url)
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        print("API Response:", data)
        if 'results' in data and data['results']:
            result = data['results'][0]
            result['id'] = symbol + str(int(time.time()))  # Cria um ID único
            return jsonify(result)
        else:
            return jsonify({'error': 'Price not found in API response'})
    except Exception as e:
        print("Error fetching quote:", e)
        return jsonify({'error': 'Failed to fetch quote. Please try again later.'}), 500
    
#salva no banco

@rotacarteira.route('/save_data', methods=['POST'])
def save_data():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = auth.get_account_info(session['user'])['users'][0]['localId']
    data = request.get_json()
    db.child("users").child(user_id).child("carteira").set(data)
    return jsonify({'success': True})

#carrega do banco

@rotacarteira.route('/load_data', methods=['GET'])
def load_data():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = auth.get_account_info(session['user'])['users'][0]['localId']
    user_data = db.child("users").child(user_id).child("carteira").get().val()
    return jsonify(user_data)

#delete do banco

@rotacarteira.route('/delete_data', methods=['POST'])
def delete_data():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = auth.get_account_info(session['user'])['users'][0]['localId']
    data = request.get_json()
    item_id = data['id']
    db.child("users").child(user_id).child("carteira").child(item_id).remove()
    return jsonify({'success': True})