import pytest
from main import app  # Importa o aplicativo Flask

@pytest.fixture
def client():
    """Configura o cliente de teste do Flask."""
    with app.test_client() as client:
        yield client

def test_first_page(client):
    """Testa a rota '/'."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'first' in response.data  # Verifica se 'first' está presente no HTML

def test_iniciante_redirect(client):
    """Testa a rota '/iniciante' para redirecionamento quando não logado."""
    response = client.get('/iniciante')
    assert response.status_code == 302  # Verifica redirecionamento
    assert b'login' in response.headers['Location']  # Verifica se redireciona para a página de login

def test_intermediario_redirect(client):
    """Testa a rota '/intermediario' para redirecionamento quando não logado."""
    response = client.get('/intermediario')
    assert response.status_code == 302
    assert b'login' in response.headers['Location']

def test_avancado_redirect(client):
    """Testa a rota '/avançado' para redirecionamento quando não logado."""
    response = client.get('/avançado')
    assert response.status_code == 302
    assert b'login' in response.headers['Location']

def test_indexcalculadora_redirect(client):
    """Testa a rota '/indexcalculadora' para redirecionamento quando não logado."""
    response = client.get('/indexcalculadora')
    assert response.status_code == 302
    assert b'login' in response.headers['Location']
