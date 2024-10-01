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
    assert b'investidor' in response.data  # Verifica se 'investidor' está presente no HTML

def test_grafico_redirect(client):
    """Testa a rota '/iniciante' para redirecionamento quando não logado."""
    response = client.get('/indexgrafico')
    assert response.status_code == 302  # Verifica redirecionamento
    assert 'login' in response.headers['Location']  # Verifica se redireciona para a página de login


def test_fundos_redirect(client):
    response = client.get('/indexfundos')
    assert response.status_code == 302
    assert 'login' in response.headers['Location']


def test_indexcalculadora_redirect(client):
    response = client.get('/indexcalculadora')
    assert response.status_code == 302
    assert 'login' in response.headers['Location']

