import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# Função para calcular o valor presente de fluxos de caixa
def calcular_valor_presente(fluxos, taxa):
    return [cf / ((1 + taxa) ** (t + 1)) for t, cf in enumerate(fluxos)]

# Função para calcular peso dps valores presente
def peso_valor_presente(valor_presente, total):
    return [value/total for value in valor_presente]

# Função para calcular peso dps valores presente (sua soma é o Macaulay duration)
def peso_por_periodo(peso_lista):
    return [periodo*peso for periodo, peso in enumerate(peso_lista)]

# Função para calcular Duration
def calcular_duration(fluxos, taxa):
    vp_total = sum(calcular_valor_presente(fluxos, taxa))
    duration = sum((t + 1) * (cf / ((1 + taxa) ** (t + 1))) for t, cf in enumerate(fluxos)) / vp_total 
    return duration

# Função para calcular Convexity
def calcular_convexity(fluxos, taxa):
    vp_total = sum(calcular_valor_presente(fluxos, taxa))
    convexity = sum(
        (cf * (t + 1) * (t + 2)) / ((1 + taxa) ** (t + 3)) for t, cf in enumerate(fluxos)
    ) / vp_total
    return convexity

# Função para gerar fluxos de caixa
def gerar_fluxos_juros(periodos, valor_inicial, taxa_anual):
    return [round(valor_inicial * ((1 + taxa_anual)**t), 2)for t in range(1, periodos + 1)]

# Função para gerar fluxos de desconto
def gerar_fluxos_descontos(periodos, valor_mensal, taxa_desconto):
    return [round(valor_mensal / ((1 + taxa_desconto)**t), 2) for t in range(1, periodos + 1)]

# Constroi Tabela de cenário determinado por uma variância
def constroi_cenario(duration, convexity, variancia, taxa, total):
    # Construir cenário de variação de juros ao redor da taxa base
    variancia_juros = [
        taxa - variancia * (5 - t) if t < 5 else 
        taxa if t == 5 else 
        taxa + variancia * (t - 5) 
        for t in range(11)
    ]
    
    # Calcular preços baseados em Duration
    preco_titulo_duration = [
        total * (1 - duration * (variancia_juros[t] - taxa))
        for t in range(11)
    ]
    
    # Calcular preços baseados em Duration + Convexity
    preco_titulo_convexity = [
        total * (1 - duration * (variancia_juros[t] - taxa) + 
                 0.5 * convexity * (variancia_juros[t] - taxa)**2)
        for t in range(11)
    ]
    
    # Garantir que o preço no ponto base (taxa inalterada) seja exatamente o total
    preco_titulo_duration[5] = total
    preco_titulo_convexity[5] = total

    # Retornar como DataFrame expandido
    return pd.DataFrame({
        'Variacao Taxa': variancia_juros,
        'Preco Duration': preco_titulo_duration,
        'Preco Convexity': preco_titulo_convexity
    })

def formatar_percentual(x, _):
    return f"{x*100:.0f}%"

def formatar_preco(x, _):
    return f"{x / 1_000_000:.1f}M"

def interest_rate_graph(duration_convexity_data, variation):
    # Configuração dos gráficos 
    plt.style.use('_mpl-gallery')
    fig, axs = plt.subplots(len(duration_convexity_data), 1, figsize=(18, 22), sharex=True)
    fig.suptitle('Duration e Convexity por Ativo', fontsize=16)

    for i, (index, row) in enumerate(duration_convexity_data.iterrows()):
        ativo = row['Ativo']
        duration = row['Duration']
        convexity = row['Convexity']
        taxa = row['Taxa']
        total = row['Total']

        df_data = constroi_cenario(duration, convexity, variation, taxa, total)
        y = df_data['Preco Duration']
        y2 = df_data['Preco Convexity']
        x = df_data['Variacao Taxa']

        # Gráfico individual
        axs[i].plot(x, y, marker='o', label=f'Duration', color='blue', linestyle='--', linewidth=2)
        axs[i].plot(x, y2, marker='x', label=f'Convexity', color='orange', linestyle='-', linewidth=2)

    # Configurações do subplot
        axs[i].xaxis.set_major_formatter(FuncFormatter(formatar_percentual))
        axs[i].yaxis.set_major_formatter(FuncFormatter(formatar_preco))
        axs[i].set_title(f'{ativo} (Taxa Base: {taxa:.2%})', fontsize=14)
        axs[i].set_xlabel('Variação da Taxa de Juros (%)', fontsize=12)
        axs[i].set_ylabel('Preço do Ativo (R$)', fontsize=12)
        axs[i].legend(loc='upper left', fontsize=10)
        axs[i].grid(True, linestyle='--', alpha=0.6)


    # Ajusta para evitar sobreposição
    plt.tight_layout(rect=[0, 0, 1, 0.95])  
    plt.show()