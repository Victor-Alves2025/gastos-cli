import pytest
from src.app import adicionar_gasto, listar_gastos, total_gastos


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
