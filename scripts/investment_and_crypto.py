# Imports embutidos
from datetime import datetime, timedelta

# Imports de bibliotecas externas
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.optimize import minimize
import yfinance as yf

# Função para definir o período -----------------------------------------------------------------------
def definir_periodo(escolha):
    """Define o período de análise com base na escolha do usuário."""
    fim = datetime.now()
    
    if escolha.endswith("M"):
        meses = int(escolha[:-1])
        if meses > 60:
            raise ValueError("O período máximo permitido é de 60 meses (5 anos).")
        inicio = fim - timedelta(days=30 * meses)
    
    elif escolha.endswith("Y"):
        anos = int(escolha[:-1])
        if anos > 5:
            raise ValueError("O período máximo permitido é de 5 anos.")
        inicio = fim - timedelta(days=365 * anos)
    
    else:
        raise ValueError("Escolha inválida! Use '<n>M' para meses ou '<n>Y' para anos.")
    
    return inicio, fim

# Função para baixar os dados --------------------------------------------------------------------------
def baixar_dados(escolhas, periodo):
    """Baixa os dados históricos dos ativos escolhidos no período definido."""
    inicio, fim = definir_periodo(periodo)
    try:
        dados = yf.download(escolhas, start=inicio, end=fim.strftime('%Y-%m-%d'))["Adj Close"]
        if dados.empty:
            raise ValueError("Nenhum dado foi baixado para os ativos selecionados.")
        return dados.dropna()
    except Exception as e:
        print(f"Erro ao baixar dados para {escolhas}: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro


# Funções para calcular os retornos e a carteira -------------------------------------------------------
def carteira_pesos_iguais(retornos):
    """Calcula a carteira de pesos iguais e o retorno acumulado."""
    num_ativos = len(retornos.columns)
    pesos = np.array([1 / num_ativos] * num_ativos)
    retorno_carteira = (retornos @ pesos).cumsum()  # Retorno acumulado
    return pesos, retorno_carteira

def carteira_otimizada_volatilidade(retornos):
    """Calcula a carteira otimizada minimizando a volatilidade."""
    cov_matrix = retornos.cov()  # Matriz de covariância diária
    num_ativos = len(retornos.columns)

    # Função objetivo: minimizar a volatilidade
    def objetivo(pesos):
        return np.sqrt(np.dot(pesos.T, np.dot(cov_matrix * 252, pesos)))  # Anualizar matriz dentro do cálculo

    restricao = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    limites = tuple((0, 1) for _ in range(num_ativos))
    pesos_iniciais = np.array([1 / num_ativos] * num_ativos)

    resultado = minimize(objetivo, pesos_iniciais, method="SLSQP", bounds=limites, constraints=restricao)
    pesos = resultado.x
    retorno_carteira = (retornos @ pesos).cumsum()  # Retorno acumulado
    return pesos, retorno_carteira

def carteira_otimizada_sharpe(retornos):
    """Calcula a carteira otimizada maximizando o índice de Sharpe."""
    cov_matrix = retornos.cov()  # Matriz de covariância diária
    retorno_medio = retornos.mean()  # Retornos médios diários
    num_ativos = len(retornos.columns)

    # Função objetivo: maximizar o índice de Sharpe
    def objetivo(pesos):
        retorno_portfolio = np.dot(pesos, retorno_medio * 252)  # Anualizar retornos dentro do cálculo
        risco_portfolio = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix * 252, pesos)))  # Anualizar matriz dentro do cálculo
        if risco_portfolio == 0:
            return np.inf  # Evitar divisão por zero
        sharpe_ratio = retorno_portfolio / risco_portfolio
        return -sharpe_ratio  # Maximizar Sharpe é equivalente a minimizar seu negativo

    restricao = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    limites = tuple((0, 1) for _ in range(num_ativos))
    pesos_iniciais = np.array([1 / num_ativos] * num_ativos)

    resultado = minimize(objetivo, pesos_iniciais, method="SLSQP", bounds=limites, constraints=restricao)
    pesos = resultado.x
    retorno_carteira = (retornos @ pesos).cumsum()  # Retorno acumulado
    return pesos, retorno_carteira

# Funções para gerar matriz -----------------------------------------------------------------------
def gerar_matriz_correlacao(retornos):
    """Gera a matriz de correlação e a exibe como um heatmap."""
    correlacao = retornos.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlacao, annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
    plt.title("Matriz de Correlação dos Ativos Selecionados")
    plt.show()
    return correlacao

# Funções para gerar gráficos -----------------------------------------------------------------------
def grafico_investment(retorno_iguais, retorno_otimizado, retorno_ibov, periodo_escolhido):
    """Gera o gráfico de comparação de retornos acumulados para investment_risk."""
    plt.figure(figsize=(14, 8))

    # Valores finais
    final_values = {
        "Carteira Otimizada": (retorno_otimizado.iloc[-1].item(), "green"),
        "Carteira Pesos Iguais": (retorno_iguais.iloc[-1].item(), "lightgreen"),
        "IBOVESPA (BOVA11)": (retorno_ibov.iloc[-1].item(), "blue"),
    }

    # Plotar retornos acumulados
    plt.plot(retorno_otimizado, label=f"Carteira Otimizada ({final_values['Carteira Otimizada'][0]:+.2%})", color="green")
    plt.plot(retorno_iguais, label=f"Carteira Pesos Iguais ({final_values['Carteira Pesos Iguais'][0]:+.2%})", color="lightgreen", linestyle="--")
    plt.plot(retorno_ibov, label=f"IBOVESPA ({final_values['IBOVESPA (BOVA11)'][0]:+.2%})", color="blue")

    # Adicionar rótulos finais no gráfico
    for label, (value, color) in final_values.items():
        bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="none", facecolor=color, alpha=0.6)
        plt.text(retorno_otimizado.index[-1], value, f"{value:+.2%}",
                 fontsize=12, color="white", ha="left", va="center", bbox=bbox_props)

    # Configuração do gráfico
    configurar_grafico(periodo_escolhido, "Comparação de Carteiras", "Retorno Acumulado (%)")


def grafico_crypto(retorno_iguais, retorno_otimizado, retorno_sp500, retorno_ouro, periodo_escolhido):
    """Gera o gráfico de comparação de retornos acumulados para crypto_risk."""
    plt.figure(figsize=(14, 8))

    # Valores finais
    final_values = {
        "Carteira Otimizada": (retorno_otimizado.iloc[-1].item(), "green"),
        "Carteira Pesos Iguais": (retorno_iguais.iloc[-1].item(), "lightgreen"),
        "S&P 500": (retorno_sp500.iloc[-1].item(), "blue"),
        "Ouro": (retorno_ouro.iloc[-1].item(), "orange"),
    }

    # Plotar retornos acumulados
    plt.plot(retorno_otimizado, label=f"Carteira Otimizada ({final_values['Carteira Otimizada'][0]:+.2%})", color="green")
    plt.plot(retorno_iguais, label=f"Carteira Pesos Iguais ({final_values['Carteira Pesos Iguais'][0]:+.2%})", color="lightgreen", linestyle="--")
    plt.plot(retorno_sp500, label=f"S&P 500 ({final_values['S&P 500'][0]:+.2%})", color="blue")
    plt.plot(retorno_ouro, label=f"Ouro ({final_values['Ouro'][0]:+.2%})", color="orange")

    # Adicionar rótulos finais no gráfico
    for label, (value, color) in final_values.items():
        bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="none", facecolor=color, alpha=0.6)
        plt.text(retorno_otimizado.index[-1], value, f"{value:+.2%}",
                 fontsize=12, color="white", ha="left", va="center", bbox=bbox_props)

    # Configuração do gráfico
    configurar_grafico(periodo_escolhido, "Comparação de Retornos Acumulados", "Retorno Acumulado (%)")

def configurar_grafico(periodo_escolhido, titulo, ylabel):
    """Configura o gráfico com base no período e estilo desejado."""
    # Linha no eixo zero
    plt.axhline(0, color="gray", linestyle="--", linewidth=1, alpha=0.8)

    # Configuração do eixo Y (em porcentagem)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))

    # Ajuste dinâmico do eixo X com base no período
    if periodo_escolhido.endswith("M"):
        meses = int(periodo_escolhido[:-1])
        if meses <= 12:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        elif meses <= 24:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        elif meses <= 36:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        else:
            plt.gca().xaxis.set_major_locator(mdates.YearLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    elif periodo_escolhido.endswith("Y"):
        anos = int(periodo_escolhido[:-1])
        if anos <= 1:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        elif anos <= 2:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        elif anos <= 3:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        else:
            plt.gca().xaxis.set_major_locator(mdates.YearLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Configurações finais
    plt.title(titulo)
    plt.xlabel("Período")
    plt.ylabel(ylabel)
    plt.legend(loc="upper left")
    plt.grid()
    plt.show()
