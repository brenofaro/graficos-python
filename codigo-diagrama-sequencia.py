import matplotlib.pyplot as plt
import pandas as pd

# Definindo os dados do projeto
atividades = [
    {'Fase': 'Iniciação', 'Inicio': '2024-07-04', 'Duracao': 14},
    {'Fase': 'Planejamento', 'Inicio': '2024-07-18', 'Duracao': 14},
    {'Fase': 'Análise de Requisitos', 'Inicio': '2024-08-01', 'Duracao': 28},
    {'Fase': 'Design do Sistema', 'Inicio': '2024-08-29', 'Duracao': 28},
    {'Fase': 'Implementação', 'Inicio': '2024-09-26', 'Duracao': 56},
    {'Fase': 'Testes', 'Inicio': '2024-11-21', 'Duracao': 28},
    {'Fase': 'Implantação', 'Inicio': '2024-12-19', 'Duracao': 14},
    {'Fase': 'Treinamento', 'Inicio': '2025-01-02', 'Duracao': 7},
    {'Fase': 'Encerramento', 'Inicio': '2025-01-09', 'Duracao': 7},
]

# Convertendo os dados em um DataFrame
df = pd.DataFrame(atividades)
df['Inicio'] = pd.to_datetime(df['Inicio'])
df['Fim'] = df['Inicio'] + pd.to_timedelta(df['Duracao'], unit='d')

# Definindo a data inicial do projeto
inicio_projeto = df['Inicio'].min()

# Calculando as semanas desde o início do projeto
df['Semanas_Inicio'] = (df['Inicio'] - inicio_projeto).dt.days // 7 + 1
df['Semanas_Fim'] = (df['Fim'] - inicio_projeto).dt.days // 7 + 1

# Criando o gráfico de barras (Gantt simplificado)
fig, ax = plt.subplots(figsize=(10, 6))

# Adicionando as barras
for i, row in df.iterrows():
    ax.barh(row['Fase'], row['Semanas_Fim'] - row['Semanas_Inicio'], left=row['Semanas_Inicio'], color='lightgreen', edgecolor='black')

# Marcadores de marcos (milestones) com numeração começando de M1
milestones = {3: 'Iniciação', 5: 'Planejamento', 9: 'Análise de Requisitos', 13: 'Design do Sistema', 17: 'Implementação', 21: 'Implementação', 25: 'Testes'}

milestone_number = 1  # Inicializando o número dos milestones com 1
for milestone, fase in milestones.items():
    ax.text(milestone, fase, f'M{milestone_number}', ha='center', va='center', color='black', fontweight='bold')
    milestone_number += 1  # Incrementando o número dos milestones

# Configurações do eixo X e Y
ax.set_xlabel('Semanas')
ax.set_xticks(range(1, df['Semanas_Fim'].max() + 1))
ax.set_ylabel('Fases')
ax.set_title('Diagrama de Barras de Atividades')

# Adicionando uma grade
ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)

plt.tight_layout()
plt.show()
