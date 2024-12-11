import pytest
from scripts.assets import ativos

def test_ativos_tipo():
    """Verifica se 'ativos' é um dicionário."""
    assert isinstance(ativos, dict), "Ativos deve ser um dicionário"

def test_ativos_nao_vazio():
    """Verifica se 'ativos' não está vazio."""
    assert len(ativos) > 0, "Ativos não deve estar vazio"

def test_chaves_principais():
    """Verifica se as chaves principais estão presentes."""
    chaves_esperadas = ["IBOVESPA", "S&P 500", "OURO"]
    for chave in chaves_esperadas:
        assert chave in ativos, f"Chave '{chave}' deve estar presente nos ativos"
