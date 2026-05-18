import pytest
from unittest.mock import patch, MagicMock
from src.app import (
    adicionar_gasto,
    listar_gastos,
    total_gastos,
    buscar_cotacao,
    converter_para_brl,
)


# Testes unitários existentes

def test_adicionar_gasto():
    adicionar_gasto(10, "teste")
    gastos = listar_gastos()
    assert gastos[-1]["valor"] == 10


def test_valor_negativo():
    with pytest.raises(ValueError):
        adicionar_gasto(-5, "erro")


def test_total():
    adicionar_gasto(20, "teste total")
    assert total_gastos() >= 20


# Testes de integração (com mock da API)

RESPOSTA_API_MOCK = {
    "USDBRL": {
        "name": "Dólar Americano/Real Brasileiro",
        "bid": "5.75",
        "ask": "5.76",
    }
}


def test_buscar_cotacao_sucesso():
    """Valida que buscar_cotacao retorna estrutura correta."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = RESPOSTA_API_MOCK
    mock_resp.raise_for_status = MagicMock()

    with patch("src.app.requests.get", return_value=mock_resp) as mock_get:
        resultado = buscar_cotacao("USD-BRL")

    mock_get.assert_called_once()
    assert resultado is not None
    assert "bid" in resultado
    assert "ask" in resultado
    assert "nome" in resultado
    assert isinstance(resultado["bid"], float)
    assert isinstance(resultado["ask"], float)
    assert resultado["bid"] == 5.75
    assert resultado["ask"] == 5.76


def test_buscar_cotacao_falha_de_rede():
    """Valida que buscar_cotacao retorna None quando a API está inacessível."""
    import requests as req
    with patch("src.app.requests.get", side_effect=req.ConnectionError):
        resultado = buscar_cotacao("USD-BRL")
    assert resultado is None


def test_buscar_cotacao_resposta_invalida():
    """Valida que retorna None quando a API retorna dado inesperado."""
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {}  # chave ausente

    with patch("src.app.requests.get", return_value=mock_resp):
        resultado = buscar_cotacao("USD-BRL")
    assert resultado is None


def test_converter_para_brl():
    """Valida que a conversão multiplica corretamente pelo bid da cotação."""
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = RESPOSTA_API_MOCK

    with patch("src.app.requests.get", return_value=mock_resp):
        valor_brl, cotacao = converter_para_brl(100, "USD-BRL")

    assert cotacao == 5.75
    assert valor_brl == round(100 * 5.75, 2)


def test_converter_para_brl_sem_conexao():
    """Valida que converter_para_brl retorna (None, None) sem conexão."""
    import requests as req
    with patch("src.app.requests.get", side_effect=req.ConnectionError):
        valor_brl, cotacao = converter_para_brl(100, "USD-BRL")
    assert valor_brl is None
    assert cotacao is None
