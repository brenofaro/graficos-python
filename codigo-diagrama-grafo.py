import networkx as nx
import pandas as pd
from pyvis.network import Network
from datetime import datetime

# Dados do projeto
atividades = [
    {'Tarefa': 'T1', 'Inicio': '2024-07-04', 'Duracao': 8},
    {'Tarefa': 'T2', 'Inicio': '2024-07-04', 'Duracao': 15},
    {'Tarefa': 'T3', 'Inicio': '2024-07-18', 'Duracao': 15},
    {'Tarefa': 'T4', 'Inicio': '2024-07-04', 'Duracao': 10},
    {'Tarefa': 'T5', 'Inicio': '2024-08-11', 'Duracao': 10},
    {'Tarefa': 'T6', 'Inicio': '2024-08-04', 'Duracao': 5},
    {'Tarefa': 'T7', 'Inicio': '2024-07-25', 'Duracao': 20},
    {'Tarefa': 'T8', 'Inicio': '2024-08-18', 'Duracao': 25},
    {'Tarefa': 'T9', 'Inicio': '2024-08-04', 'Duracao': 15},
    {'Tarefa': 'T10', 'Inicio': '2024-08-11', 'Duracao': 15},
    {'Tarefa': 'T11', 'Inicio': '2024-08-25', 'Duracao': 7},
    {'Tarefa': 'T12', 'Inicio': '2024-09-05', 'Duracao': 10},
]

# Convertendo para DataFrame
df = pd.DataFrame(atividades)
df['Inicio'] = pd.to_datetime(df['Inicio'])
df['Fim'] = df['Inicio'] + pd.to_timedelta(df['Duracao'], unit='d')

# Criando o grafo de atividades
G = nx.DiGraph()

# Adicionando nó inicial e final
inicio_projeto = df['Inicio'].min().strftime('%d/%m/%Y')
fim_projeto = df['Fim'].max().strftime('%d/%m/%Y')
G.add_node('Start', label='Start', title=f"Início do Projeto: {inicio_projeto}", shape='ellipse', color='lightgreen')
G.add_node('Finish', label='Finish', title=f"Término do Projeto: {fim_projeto}", shape='ellipse', color='lightgreen')

# Adicionando as tarefas como nós
for _, row in df.iterrows():
    G.add_node(
        row['Tarefa'],
        label=row['Tarefa'],
        title=f"Duração: {row['Duracao']} dias\nFim: {row['Fim'].strftime('%d/%m/%Y')}",
        shape='box',
        color='lightblue',
        size=25
    )

# Definindo as conexões (arestas) entre as tarefas e incluindo o início e fim
arestas = [
    ('Start', 'T1'), ('Start', 'T2'), ('Start', 'T4'),
    ('T1', 'T3'), ('T1', 'T4'), ('T2', 'T5'), ('T2', 'T7'),
    ('T3', 'T9'), ('T4', 'T5'), ('T6', 'T9'), ('T7', 'T10'),
    ('T5', 'T8'), ('T9', 'T11'), ('T10', 'T12'), ('T11', 'T12'),
    ('T8', 'Finish'), ('T12', 'Finish')
]

G.add_edges_from(arestas)

# Definindo marcos
milestones = {'T3': 'M1', 'T5': 'M2', 'T7': 'M3', 'T9': 'M4', 'T10': 'M5', 'T12': 'M6'}
for tarefa, marco in milestones.items():
    if tarefa in G.nodes:
        G.nodes[tarefa]['title'] += f"\nMarco: {marco}"
        G.nodes[tarefa]['label'] = f"{tarefa}\n{marco}"

# Criando a visualização com PyVis
net = Network(height='800px', width='100%', directed=True, notebook=False, bgcolor='#ffffff', font_color='black')

# Configurando o layout para permitir arrastar nós
net.barnes_hut()

# Adicionando os nós e arestas ao objeto PyVis
for node, data in G.nodes(data=True):
    net.add_node(
        node,
        label=data.get('label', node),
        title=data.get('title', ''),
        shape=data.get('shape', 'ellipse'),
        color=data.get('color', 'lightblue'),
        size=data.get('size', 25)
    )

for source, target in G.edges():
    net.add_edge(source, target, arrows='to')

# Configurações adicionais para melhorar a interface
net.set_options("""
var options = {
  "nodes": {
    "font": {
      "size": 14,
      "strokeWidth": 2
    }
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "arrows": {
      "to": {
        "enabled": true,
        "scaleFactor": 1
      }
    },
    "smooth": {
      "enabled": true,
      "type": "continuous"
    }
  },
  "physics": {
    "enabled": true,
    "barnesHut": {
      "gravitationalConstant": -8000,
      "springConstant": 0.04,
      "springLength": 250
    },
    "minVelocity": 0.75
  }
}
""")

# Gerando e salvando o grafo interativo em HTML
net.show('grafo_projeto.html', notebook=False)

