import math
import pandas as pd

def demander_type_filetage():
    reponse = input("Avez-vous un filetage métrique ou à gaz? Tapez 'métrique' ou 'gaz': ").strip().lower()
    
    while reponse not in ['métrique', 'gaz']:
        print("Réponse non valide. Veuillez taper 'métrique' ou 'gaz'.")
        reponse = input("Avez-vous un filetage métrique ou à gaz? Tapez 'métrique' ou 'gaz': ").strip().lower()
    
    return reponse

def trouver_entiers_adjacents(nombre):
    inf = math.floor(nombre)
    sup = math.ceil(nombre)
    if inf == sup:
        inf -= 1
        sup += 1
    return inf, sup

def pas_metrique(inf, sup):
    df = pd.read_csv('Metrique.csv', header=None)
    df.columns = ['Type', 'Taille', 'Valeur']
    pattern = f"M{inf}"
    selected_values = {}
    for size in df['Taille'].unique():
        if size.startswith(pattern) or size == f"M{sup}":
            selected_values[size] = df[df['Taille'] == size]['Valeur'].iloc[0]

    for taille, valeur in selected_values.items():
        print(f"{taille}: {valeur}")

pas_metrique(2, 3)
