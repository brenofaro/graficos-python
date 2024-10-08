import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Definindo os dados do projeto
atividades = [
    {'Fase': 'Iniciação', 'Responsáveis': ['Rômulo'], 'Inicio': '2024-07-04', 'Duracao': 14},
    {'Fase': 'Planejamento', 'Responsáveis': ['Rômulo'], 'Inicio': '2024-07-18', 'Duracao': 14},
    {'Fase': 'Análise de Requisitos', 'Responsáveis': ['Brenno', 'Newton'], 'Inicio': '2024-08-01', 'Duracao': 28},
    {'Fase': 'Design do Sistema', 'Responsáveis': ['Brenno', 'Newton'], 'Inicio': '2024-08-29', 'Duracao': 28},
    {'Fase': 'Implementação', 'Responsáveis': ['Itor', 'Heitor', 'Humberto', 'Davi'], 'Inicio': '2024-09-26', 'Duracao': 56},
    {'Fase': 'Testes', 'Responsáveis': ['Itor', 'Heitor'], 'Inicio': '2024-11-21', 'Duracao': 28},
    {'Fase': 'Implantação', 'Responsáveis': ['Itor', 'Humberto'], 'Inicio': '2024-12-19', 'Duracao': 14},
    {'Fase': 'Treinamento', 'Responsáveis': ['Rômulo'], 'Inicio': '2025-01-02', 'Duracao': 7},
    {'Fase': 'Encerramento', 'Responsáveis': ['Rômulo'], 'Inicio': '2025-01-09', 'Duracao': 7},
]

# Convertendo os dados em um DataFrame
df = pd.DataFrame(atividades)
df['Inicio'] = pd.to_datetime(df['Inicio'])
df['Fim'] = df['Inicio'] + pd.to_timedelta(df['Duracao'], unit='d')

# Definindo a data inicial do projeto
inicio_projeto = df['Inicio'].min()

# Calculando as semanas desde o início do projeto
df['Semanas_Inicio'] = (df['Inicio'] - inicio_projeto).dt.days // 7
df['Semanas_Fim'] = (df['Fim'] - inicio_projeto).dt.days // 7

# Criando o gráfico de Gantt
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightpink', 'lightyellow', 'lightgrey', 'wheat', 'plum']

for i, atividade in df.iterrows():
    ax.barh(atividade['Responsáveis'], atividade['Semanas_Fim'] - atividade['Semanas_Inicio'], 
            left=atividade['Semanas_Inicio'], color=colors[i % len(colors)], edgecolor='black', 
            linewidth=1.5, align='center', label=atividade['Fase'] if i == 0 or atividade['Fase'] not in df['Fase'][:i].values else '')

# Configurações do eixo X para exibir as semanas desde o início do projeto
ax.set_xticks(range(0, df['Semanas_Fim'].max() + 1))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)+1}'))

# Adicionando legenda para descrever cada fase na parte superior esquerda
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(0, 1), title='Fases do Projeto')

# Adicionando a grade (grid)
#ax.grid(axis='x', linestyle='--', linewidth=0.7, color='gray')

# Configurações do gráfico
ax.set_ylabel('Equipe')
ax.set_xlabel('Semanas')
ax.set_title('Alocação da Equipe - Projeto de Desenvolvimento de Software')
plt.tight_layout()

# Exibindo o gráfico
plt.show()
