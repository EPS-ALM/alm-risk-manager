import pytest
import pandas as pd
import numpy as np

from scripts.interestRiskLib import (
    calcular_valor_presente,
    peso_valor_presente,
    peso_por_periodo,
    calcular_duration,
    calcular_convexity,
    gerar_fluxos_juros,
    gerar_fluxos_descontos,
    constroi_cenario
)

# Dados mockados
ativo = [4, 1_000_000_000, 0.0015]
fluxo_ativo = [1001500000.0, 1003002250.0, 1004506753.38, 1006013513.51]
valor_presente = [1000000000.0, 999999999.9999998, 1000000000.0049775, 1000000000.0049077]
total = 4000000000.009885
peso = [0.2499999999993822,0.24999999999938213, 0.25000000000062655, 0.2500000000006091]
peso_periodo = [0.2499999999993822, 0.49999999999876427, 0.7500000000018796, 1.0000000000024365]

passivo = [3, 1_000_000, 0.012]
fluxo_passivo = [988142.29, 976425.19, 964847.03]

def test_gerar_fluxos_descontos():
    assert fluxo_passivo == gerar_fluxos_descontos(passivo[0], passivo[1], passivo[2]), 'Fluxo deve ser igual ao dado mockado'
    assert None == gerar_fluxos_descontos(-1, passivo[1], passivo[2]), 'Argumentos devem pertencer aos naturais'
    assert [] != gerar_fluxos_descontos(passivo[0], passivo[1], passivo[2]), 'Não deve ter retorno vazio'

def test_gerar_fluxos_juros():
    assert fluxo_ativo == gerar_fluxos_juros(ativo[0], ativo[1], ativo[2]), 'Fluxo deve ser igual ao dado mockado'
    assert None == gerar_fluxos_juros(ativo[0], ativo[1], 0), 'Argumentos devem pertencer aos naturais e a taxa não pode ser 0'
    assert [] != gerar_fluxos_juros(ativo[0], ativo[1], ativo[2]), 'Não deve ter retorno vazio'

def test_calcular_valor_presente():
    assert valor_presente == calcular_valor_presente(fluxo_ativo, ativo[2]), 'Valores presentes devem ser igual aos dados mockados'
    assert [] != calcular_valor_presente(fluxo_ativo, ativo[2]), 'Não deve retornar uma lista vazia'

def test_peso_valor_presente():
    assert peso == peso_valor_presente(valor_presente, sum(valor_presente)), 'Pesos devem ser igual aos dados mockados'
    assert [] != peso_valor_presente(valor_presente, sum(valor_presente)), 'Não deve retornar uma lista vazia'

def test_peso_por_periodo():
    assert peso_periodo == peso_por_periodo(peso), 'Pesos por periodo devem ser igual aos dados mockados'
    assert [] != peso_por_periodo(peso), 'Não deve retornar uma lista vazia'

def test_calcular_duration():
    f = [100,200,300,400,1000]
    assert 3.9246839314451263 == calcular_duration(f, 0.05), "Valida valor da duration"
    assert not 0 >= calcular_duration(f, 0.05), "Duration deve ser maior que zero"

def test_calcular_convexity():
    f = [100,200,300,400,1000]
    assert 18.970408715688645 == calcular_convexity(f, 0.05), "Valida valor da convexity"
    assert not 0 >= calcular_convexity(f, 0.05), "Convexity deve ser maior que zero"

# Verificar o formato do DataFrame retornado
def test_constroi_cenario_formato():
    duration = 5
    convexity = 10
    variancia = 0.01
    taxa = 0.05
    total = 1000

    df = constroi_cenario(duration, convexity, variancia, taxa, total)

    
    assert isinstance(df, pd.DataFrame), "A função não retornou um DataFrame"
    assert list(df.columns) == ['Variacao Taxa', 'Preco Duration', 'Preco Convexity'], \
        "As colunas do DataFrame não correspondem ao esperado"
    assert len(df) == 11, "O número de linhas no DataFrame está incorreto"

def test_constroi_cenario_valores_basicos():
    duration = 2
    convexity = 3
    variancia = 0.01
    taxa = 0.05
    total = 1000

    df = constroi_cenario(duration, convexity, variancia, taxa, total)

    # Verificar que o preço no ponto base (taxa inalterada) é igual ao total
    assert df.loc[5, 'Preco Duration'] == total, \
        "O preço baseado em Duration no ponto base não é igual ao total"
    assert df.loc[5, 'Preco Convexity'] == total, \
        "O preço baseado em Convexity no ponto base não é igual ao total"
    
    # Verificar que a variação de taxa está correta no ponto inicial e final
    assert df.loc[0, 'Variacao Taxa'] == pytest.approx(0.05 - 0.05), \
        "A variação de taxa no início está incorreta"
    assert df.loc[10, 'Variacao Taxa'] == pytest.approx(0.05 + 0.05), \
        "A variação de taxa no final está incorreta"