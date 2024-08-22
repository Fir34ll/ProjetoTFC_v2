from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import time

from flask import Blueprint, render_template, redirect, url_for, session

rotaflls = Blueprint('rotaflls', __name__)

@rotaflls.route('/indexfundos')
def indexfundos():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('indexfundos.html')

@rotaflls.route('/available_funds', methods=['GET'])
def available_funds():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    token = 'xoAToPKAai8jfSwukJspez'
    url = f'https://brapi.dev/api/quote/list?type=fund&token={token}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        funds = [fund['stock'] for fund in data.get('stocks', [])]
        return jsonify({'funds': funds})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch available funds'}), 500

# Rota para buscar informações detalhadas de um Fundo Imobiliário
@rotaflls.route('/show_fund_info', methods=['POST'])
def show_fund_info():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    ticker = data.get('ticker')
    
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400

    token = 'xoAToPKAai8jfSwukJspez'
    url = f'https://brapi.dev/api/quote/{ticker}?token={token}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'results' in data and data['results']:
            result = data['results'][0]
            result['id'] = ticker + str(int(time.time()))
            return jsonify(result)
        else:
            print(f"API Response Error: {data}")
            return jsonify({'error': 'Price not found in API response'})
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {str(e)}")
        return jsonify({'error': 'Failed to fetch quote. Please try again later.'}), 500

