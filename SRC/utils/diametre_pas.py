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

def pas_metrique(diametre):
    # Charger les données
    df = pd.read_csv(metrique_path)
    # Assumer que le fichier CSV a des colonnes 'Type', 'Taille', 'Valeur'
    df.columns = ['Type', 'Taille', 'Valeur']

    # Obtenir les diamètres inférieurs et supérieurs en fonction de la tolérance
    inf, sup = trouver_entiers_adjacents(diametre)

    # Filtrer le DataFrame pour les tailles correspondantes avec ancrage précis
    pattern = f"^(M{inf}|M{round(diametre)}|M{sup}|MF{inf}|MF{round(diametre)}|MF{sup})$"
    # pattern = f"^(M{inf}|M{round(diametre)}|M{sup})$"
    filtered_df = df[df['Taille'].str.contains(pattern, regex=True)]

    # Afficher les résultats
    results = filtered_df.groupby('Taille')['Valeur'].apply(list).to_dict()
    
    for taille, valeurs in results.items():
        print(f"{taille}: {valeurs}")
    return results

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


