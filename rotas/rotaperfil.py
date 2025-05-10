from firebase_admin import auth, db
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from rotas.config import config
import pyrebase


rotaperfil = Blueprint('rotaperfil', __name__)
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@rotaperfil.route('/perfilinvestidor')
def perfilinvestidor():
    if 'user' not in session:
        return redirect(url_for('rotalogin.login'))
    return render_template('perfilinvestidor.html')

@rotaperfil.route('/save_investor_profile', methods=['POST'])
def save_investor_profile():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = auth.get_account_info(session['user'])['users'][0]['localId']
    result = request.get_json().get('result')

    # Atualiza o campo `perfilinvestidor` com o resultado final
    db.child("users").child(user_id).child("info").update({
        "perfilinvestidor": result
    })
    
    return jsonify({'success': True})

@rotaperfil.route('/get_investor_profile')
def get_investor_profile():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = auth.get_account_info(session['user'])['users'][0]['localId']
    user_info = db.child("users").child(user_id).child("info").get().val()
    
    if not user_info or 'perfilinvestidor' not in user_info:
        return jsonify({'error': 'Profile not found'}), 404

    profile_type = user_info['perfilinvestidor']
    
    # Define as recomendações baseadas no perfil
    if profile_type == "Conservador":
        recommendations = {
            "description": "Como investidor conservador, você prioriza a segurança e a preservação do capital. Suas recomendações são focadas em investimentos de baixo risco:",
            "investments": [
                {
                    "name": "Tesouro Direto",
                    "description": "Títulos públicos do governo federal, considerados os investimentos mais seguros do Brasil.",
                    "allocation": "40-50% do portfólio"
                },
                {
                    "name": "CDBs de Bancos Grandes",
                    "description": "Certificados de Depósito Bancário de instituições sólidas, com proteção do FGC.",
                    "allocation": "20-30% do portfólio"
                },
                {
                    "name": "Fundos DI",
                    "description": "Fundos que acompanham a taxa Selic, oferecendo boa liquidez e baixo risco.",
                    "allocation": "15-20% do portfólio"
                },
                {
                    "name": "LCI/LCA",
                    "description": "Títulos de crédito imobiliário e agrícola, isentos de IR para pessoas físicas.",
                    "allocation": "10-15% do portfólio"
                }
            ],
            "tips": [
                "Mantenha uma reserva de emergência em investimentos de alta liquidez",
                "Diversifique entre diferentes tipos de títulos de renda fixa",
                "Priorize investimentos com proteção do FGC",
                "Considere a inflação ao escolher seus investimentos"
            ]
        }
    elif profile_type == "Moderado":
        recommendations = {
            "description": "Como investidor moderado, você busca um equilíbrio entre segurança e rentabilidade. Suas recomendações incluem uma mistura de investimentos de renda fixa e variável:",
            "investments": [
                {
                    "name": "Ações Blue Chips Brasileiras",
                    "description": "Ações de empresas grandes e consolidadas: Petrobras (PETR4), Vale (VALE3), Itaú (ITUB4), Bradesco (BBDC4), B3 (B3SA3).",
                    "allocation": "15-25% do portfólio"
                },
                {
                    "name": "Fundos Imobiliários",
                    "description": "FIIs como HGLG11, KNRI11, MXRF11 - focados em imóveis comerciais e recebíveis imobiliários.",
                    "allocation": "20-30% do portfólio"
                },
                {
                    "name": "Tesouro Direto",
                    "description": "Títulos públicos para manter uma base segura no portfólio.",
                    "allocation": "25-35% do portfólio"
                },
                {
                    "name": "Ações de Dividendos",
                    "description": "Ações com histórico de bons dividendos: Taesa (TAEE11), Copel (CPLE6), Eletrobras (ELET6).",
                    "allocation": "15-20% do portfólio"
                }
            ],
            "tips": [
                "Mantenha uma base sólida em renda fixa",
                "Diversifique entre diferentes setores da economia brasileira",
                "Considere ETFs como BOVA11 para exposição ao Ibovespa",
                "Monitore regularmente a performance do seu portfólio"
            ]
        }
    else:  # Arrojado
        recommendations = {
            "description": "Como investidor arrojado, você está disposto a assumir mais riscos em busca de maiores retornos. Suas recomendações incluem uma maior exposição a ativos de renda variável:",
            "investments": [
                {
                    "name": "Ações de Crescimento",
                    "description": "Ações com alto potencial: Magazine Luiza (MGLU3), Locaweb (LWSA3), Cielo (CIEL3), Via (VIIA3).",
                    "allocation": "30-40% do portfólio"
                },
                {
                    "name": "Small Caps Brasileiras",
                    "description": "Ações de empresas menores: Méliuz (CASH3), Enjoei (ENJU3), Locaweb (LWSA3), CVC (CVCB3).",
                    "allocation": "15-25% do portfólio"
                },
                {
                    "name": "Ações de Tecnologia",
                    "description": "Ações do setor de tecnologia: TOTVS (TOTS3), Locaweb (LWSA3), Cielo (CIEL3), Méliuz (CASH3).",
                    "allocation": "20-30% do portfólio"
                },
                {
                    "name": "Ações de Commodities",
                    "description": "Ações do setor de commodities: Vale (VALE3), Petrobras (PETR4), Gerdau (GGBR4), Suzano (SUZB3).",
                    "allocation": "15-20% do portfólio"
                }
            ],
            "tips": [
                "Mantenha uma pequena parcela em renda fixa para segurança",
                "Diversifique entre diferentes setores da economia brasileira",
                "Considere ações de empresas com forte presença internacional",
                "Esteja preparado para volatilidade de curto prazo"
            ]
        }

    return jsonify({
        "result": profile_type,
        "recommendations": recommendations
    })