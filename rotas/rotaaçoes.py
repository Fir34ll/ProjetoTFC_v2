from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import time
from flask import Blueprint, render_template, redirect, url_for, session

rotaaçoes = Blueprint('rotaaçoes', __name__)

@rotaaçoes.route('/indexaçao')
def indexaçao():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('indexaçao.html')

#açoes disponiveis para mostrar na tabela
@rotaaçoes.route('/available_stocks', methods=['GET'])
def available_stocks():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    token = 'xoAToPKAai8jfSwukJspez'
    
    url = f'https://brapi.dev/api/quote/list?type=stock&token={token}?sortOrder=asc'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        stocks = [stock['stock'] for stock in data.get('stocks', [])]
        return jsonify({'stocks': stocks})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch available stocks'}), 500 

#exibe informaçoes das açoes
@rotaaçoes.route('/show_stock_info', methods=['GET', 'POST'])
def show_stock_info():
    
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    symbol = data.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400

    token = 'xoAToPKAai8jfSwukJspez'
    url = f'https://brapi.dev/api/quote/{symbol}?token={token}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'results' in data and data['results']:
            result = data['results'][0]
            result['id'] = symbol + str(int(time.time()))
            return jsonify(result)
        else:
            return jsonify({'error': 'Price not found in API response'})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch quote. Please try again later.'}), 500    
    

    
