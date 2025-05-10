from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
import requests
import time
import json

rotarecomendacao = Blueprint('rotarecomendacao', __name__)

@rotarecomendacao.route('/get_stock_info', methods=['POST'])
def get_stock_info():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    symbols = data.get('symbols', [])
    
    if not symbols:
        return jsonify({'error': 'No symbols provided'}), 400

    token = 'xoAToPKAai8jfSwukJspez'
    results = []
    
    for symbol in symbols:
        try:
            url = f'https://brapi.dev/api/quote/{symbol}?token={token}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if 'results' in data and data['results']:
                result = data['results'][0]
                stock_info = {
                    'symbol': symbol,
                    'name': result.get('longName', result.get('shortName', '')),
                    'price': result.get('regularMarketPrice', 0),
                    'change': result.get('regularMarketChangePercent', 0),
                    'logo': result.get('logourl', ''),
                    'dayHigh': result.get('regularMarketDayHigh', None),
                    'dayLow': result.get('regularMarketDayLow', None),
                    'volume': result.get('regularMarketVolume', None),
                    'marketCap': result.get('marketCap', None),
                    'priceEarnings': result.get('priceEarnings', None),
                    'earningsPerShare': result.get('earningsPerShare', None)
                }
                results.append(stock_info)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            continue

    return jsonify({'stocks': results})
