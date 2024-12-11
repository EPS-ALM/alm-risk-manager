import pytest
import pandas as pd
import numpy as np
from scripts.investment_and_crypto import (
    definir_periodo,
    baixar_dados,
    carteira_pesos_iguais,
    carteira_otimizada_volatilidade,
    carteira_otimizada_sharpe,
    gerar_matriz_correlacao,
)

def test_definir_periodo():
    """Testa a função definir_periodo."""
    inicio, fim = definir_periodo("6M")
    assert (fim - inicio).days == 180, "Período de 6M deveria ser de 180 dias"
    with pytest.raises(ValueError):
        definir_periodo("100M")  # Período inválido
    with pytest.raises(ValueError):
        definir_periodo("6X")  # Formato inválido

def test_baixar_dados():
    """Testa a função baixar_dados."""
    dados = baixar_dados(["PETR4.SA"], "1M")
    assert not dados.empty, "Os dados não deveriam estar vazios para PETR4.SA em 1M"
    assert "PETR4.SA" in dados.columns, "A coluna PETR4.SA deveria estar presente nos dados"

def test_carteira_pesos_iguais():
    """Testa a função carteira_pesos_iguais."""
    retornos = pd.DataFrame({
        "A": [0.01, -0.02, 0.03],
        "B": [-0.01, 0.02, -0.03]
    })
    pesos, retorno_carteira = carteira_pesos_iguais(retornos)
    assert np.isclose(pesos.sum(), 1.0), "Os pesos devem somar 1"
    assert len(retorno_carteira) == len(retornos), "O retorno acumulado deve ter o mesmo comprimento que os retornos"

def test_carteira_otimizada_volatilidade():
    """Testa a função carteira_otimizada_volatilidade."""
    retornos = pd.DataFrame({
        "A": [0.01, -0.02, 0.03],
        "B": [-0.01, 0.02, -0.03]
    })
    pesos, retorno_carteira = carteira_otimizada_volatilidade(retornos)
    assert np.isclose(pesos.sum(), 1.0), "Os pesos devem somar 1"
    assert len(retorno_carteira) == len(retornos), "O retorno acumulado deve ter o mesmo comprimento que os retornos"

def test_carteira_otimizada_sharpe():
    """Testa a função carteira_otimizada_sharpe."""
    retornos = pd.DataFrame({
        "A": [0.01, -0.02, 0.03],
        "B": [-0.01, 0.02, -0.03]
    })
    pesos, retorno_carteira = carteira_otimizada_sharpe(retornos)
    assert np.isclose(pesos.sum(), 1.0), "Os pesos devem somar 1"
    assert len(retorno_carteira) == len(retornos), "O retorno acumulado deve ter o mesmo comprimento que os retornos"

