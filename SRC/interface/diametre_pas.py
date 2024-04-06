def demander_type_filetage():
    reponse = input("Avez-vous un filetage métrique ou à gaz? Tapez 'métrique' ou 'gaz': ").strip().lower()
    
    while reponse not in ['métrique', 'gaz']:
        print("Réponse non valide. Veuillez taper 'métrique' ou 'gaz'.")
        reponse = input("Avez-vous un filetage métrique ou à gaz? Tapez 'métrique' ou 'gaz': ").strip().lower()
    
    return reponse

type_filetage = demander_type_filetage()
print(f"Vous avez sélectionné un filetage {type_filetage}.")
