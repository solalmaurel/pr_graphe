import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Fonction pour calculer la distance entre deux satellites
def calculate_distance(sat1, sat2):
    return np.sqrt((sat1['x'] - sat2['x'])**2 + (sat1['y'] - sat2['y'])**2 + (sat1['z'] - sat2['z'])**2)

# Fonction pour créer les connexions entre satellites en fonction de la portée
def create_connections(data, range_km):
    connections = []
    for i, sat1 in data.iterrows():
        for j, sat2 in data.iterrows():
            if i < j:  # Eviter de vérifier deux fois les mêmes combinaisons
                distance = calculate_distance(sat1, sat2)
                if distance/1000 <= range_km:
                    connections.append((sat1['sat_id'], sat2['sat_id']))
    return connections

# Fonction pour afficher le graphe en 3D
def plot_graph_3d(data, connections, title):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Afficher les satellites (points)
    ax.scatter(data['x'], data['y'], data['z'], c='b', s=20, label="Satellites")
    
    # Afficher les connexions (arêtes)
    for conn in connections:
        sat1 = data[data['sat_id'] == conn[0]].iloc[0]
        sat2 = data[data['sat_id'] == conn[1]].iloc[0]
        ax.plot([sat1['x'], sat2['x']], [sat1['y'], sat2['y']], [sat1['z'], sat2['z']], c='r', alpha=0.5)
    
    ax.set_title(title)
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    plt.legend()
    plt.show()

# Charger les données
file_path = 'topology_avg.csv'
data_avg = pd.read_csv(file_path)

# Créer les connexions pour différentes portées et afficher les graphes
for range_km in [20, 40, 60]:
    connections = create_connections(data_avg, range_km)
    plot_graph_3d(data_avg, connections, f"Graphe de l'essaim (Densité moyenne, Portée {range_km} km)")
