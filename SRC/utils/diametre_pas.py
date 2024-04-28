import math
import pandas as pd
import os


metrique_path = "Ressources\Table\Metrique.csv"
gaz_path = "Ressources\Table\Gaz.csv"

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
    df = pd.read_csv(metrique_path, header=None)
    df.columns = ['Type', 'Taille', 'Valeur']
    pattern = f"M{inf}"
    selected_values = {}
    for size in df['Taille'].unique():
        if size.startswith(pattern) or size == f"M{sup}":
            selected_values[size] = df[df['Taille'] == size]['Valeur'].iloc[0]

    for taille, valeur in selected_values.items():
        print(f"{taille}: {valeur}")


def load_csvgaz_to_df():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(dir_path, '..', '..', 'Ressources', 'Table', 'Gaz.csv')
    df = pd.read_csv(csv_path, delimiter=';', decimal=',')
    df.columns = [col.strip() for col in df.columns]
    return df


def select_possible_pitches(df, measured_diameter, tolerance=1.0):
    # Selection les diamiètre possible
    tolerance_mask = (df["Diam_mm"] >= (measured_diameter - tolerance)) & (df["Diam_mm"] <= (measured_diameter + tolerance))
    possible_pitches_df = df[tolerance_mask]

    bsp_rc_pitches = possible_pitches_df['BSP-BSPT / RC'].tolist()
    npt_pitches = possible_pitches_df['NPT'].tolist()
    pitches = bsp_rc_pitches + npt_pitches  # Combine lists
    return pitches
