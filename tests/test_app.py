import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Simula sessão logada
def login_simulado(client):
    with client.session_transaction() as sess:
        sess['user'] = 'teste@exemplo.com'

# Página inicial pública
def test_first_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'investidor' in response.data  # Verifica palavra-chave na home

# Redirecionamento para login (usuário não logado)
def test_indexcalculadora_redirect(client):
    response = client.get('/indexcalculadora')
    assert response.status_code == 302
    assert 'login' in response.headers['Location']

def test_indeximposto_redirect(client):
    response = client.get('/indeximposto')
    assert response.status_code == 302
    assert 'login' in response.headers['Location']

def test_recomendacoes_redirect(client):
    response = client.get('/recomendacoes')
    assert response.status_code == 302
    assert 'login' in response.headers['Location']

# Páginas protegidas com sessão ativa
def test_indexcalculadora_logado(client):
    login_simulado(client)
    response = client.get('/indexcalculadora')
    assert response.status_code == 200
    assert b'Calculadora' in response.data or b'calcular' in response.data

def test_indeximposto_logado(client):
    login_simulado(client)
    response = client.get('/indeximposto')
    assert response.status_code == 200
    assert b'Imposto' in response.data or b'simulador' in response.data

def test_recomendacoes_logado(client):
    login_simulado(client)
    response = client.get('/recomendacoes')
    assert response.status_code == 200
    assert b'Recomenda' in response.data or b'perfil' in response.data
