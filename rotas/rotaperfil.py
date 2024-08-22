from firebase_admin import auth, db
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify

rotaperfil = Blueprint('rotaperfil', __name__)

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