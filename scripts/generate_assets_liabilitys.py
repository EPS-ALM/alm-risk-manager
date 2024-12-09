import pandas as pd
import yfinance as yf
import random

# Função para gerar fluxos de caixa
def gerar_fluxos_juros(periodos, valor_inicial, taxa_anual):
    return [round(valor_inicial * ((1 + taxa_anual)**t), 2)for t in range(1, periodos + 1)]

# return [round(valor_inicial * ((1 + taxa_anual)**t), 2) for t in range(1, periodos + 1)]
def gerar_fluxos_descont(periodos, valor_mensal, taxa_desconto):
    return [round(valor_mensal / ((1 + taxa_desconto)**t), 2) for t in range(1, periodos + 1)]


# Lista de ativos e seus símbolos no Yahoo Finance
ativos_yh = {
    "Vale": "VALE3.SA",
    "Petrobras": "PETR4.SA",
    "Ouro": "GC=F",
    "Dólar": "USDBRL=X",
    "S&P 500": "^GSPC"
}

# Período de análise
periodo = "5y"

# Dicionário para armazenar dados
dados_ativos = {}

# Obter dados históricos para cada ativo
for nome, simbolo in ativos_yh.items():
    ticker = yf.Ticker(simbolo)
    historico = ticker.history(period=periodo)
    dados_ativos[nome] = {
        "Histórico": historico,
        "Info": ticker.info
    }


taxa_media_anual = []
for nome, dados in dados_ativos.items():
    precos = dados["Histórico"]['Close']
    retornos = precos.pct_change().dropna()
    taxa_por_item = (1 + retornos.mean())**252 - 1
    taxa_media_anual.append(taxa_por_item)
    print(f"\n{nome}: Taxa de Retorno Média Anual: {taxa_por_item:.2%}")

precos_dolar = dados_ativos["Dólar"]["Histórico"]['Close']
retornos_dolar = precos_dolar.pct_change().dropna()
taxa_cambio_anual = (1 + retornos_dolar.mean())**252 - 1
print(f"Taxa de variação do Dólar (USD/BRL): {taxa_cambio_anual:.2%}")

# Mock dos Ativos
ativos = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5],
    "Ativo": ["Vale", "Petrobras", "Ouro", "Dollar", "S&P 500"],
    "Tipo de Ativo": ["Ação", "Ação", "Commodities", "Moeda", "Índice"],
    "Valor de Mercado (R$)": [2000000, 1500000, 1000000, 500000, 1000000],
    "Datas dos Fluxos (T)": [5, 4, 6, 2, 5],
    "Taxa de Juros Atual (%)": [taxa_media_anual[0], taxa_media_anual[1], taxa_media_anual[2], taxa_media_anual[3], taxa_media_anual[4]]
})

# Mock dos Passivos
passivos = pd.DataFrame({
    "ID": [1, 2, 3],
    "Tipo de Passivo": ["Benefício Mensal", "Resgate", "Pensão de Longo Prazo"],
    "Valor Mensal (R$)": [10000, 1500, 1000],  # Valores fixos em escala mensal
    "Datas dos Fluxos (T)": [12, 12, 61],
    "Taxa de Desconto (%)": [0.5, 0.5, 0.5]
})

passivos.to_csv('../dataset/passivos.csv', index=False)
ativos.to_csv('../dataset/ativos.csv', index=False)

print("ATIVOS")
print(ativos)
print("\nPASSIVOS")
print(passivos)
