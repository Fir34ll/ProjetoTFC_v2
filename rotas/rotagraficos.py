from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import time
from flask import Blueprint, render_template, redirect, url_for, session

rotagraficos = Blueprint('rotagraficos', __name__)

#parte do grafico

@rotagraficos.route('/indexgrafico')
def indexgrafico():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('indexgrafico.html')

@rotagraficos.route('/get_quote2', methods=['POST'])
def get_quote2():
    data = request.json
    symbol = data.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400

    token = 'xoAToPKAai8jfSwukJspez'  # Substitua pelo seu token da API real
    url = f'https://brapi.dev/api/quote/{symbol}?range=3mo&interval=1d&token={token}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        api_data = response.json()

        # Log da resposta para depuração
        print("API Response:", api_data)

        # Verificar se 'results' está presente e contém dados
        if 'results' in api_data and len(api_data['results']) > 0:
            result = api_data['results'][0]
            historical_data = result.get('historicalDataPrice', [])

            # Formatar os dados para o gráfico
            formatted_data = [{
                'date': item['date'],
                'open': item['open'],
                'high': item['high'],
                'low': item['low'],
                'close': item['close']
            } for item in historical_data]

            return jsonify({
                'symbol': result['symbol'],
                'historicalDataPrice': formatted_data
            })
        else:
            return jsonify({'error': 'No results found in API response'})
    except requests.RequestException as e:
        print("Error fetching quote:", e)
        return jsonify({'error': 'Failed to fetch quote. Please try again later.'}), 500

