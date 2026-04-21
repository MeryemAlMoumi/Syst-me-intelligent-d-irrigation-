import joblib

# Chargement des modèles IA
clf_anomalie = joblib.load("models_ai/modele_ferme.pkl")
clf_solution = joblib.load("models_ai/model_solution.pkl")

# Mapping ID → Texte
id_to_label = {
    -1: "anomalie_detectee",
     0: "normal",
     1: "fuite",
     2: "obstruction",
     3: "pompe_defaillante"
}


def analyser_par_ai(pression: float, debit: float, humidite: float):

    X = [[pression, debit, humidite]]

    anomalie_id = clf_anomalie.predict(X)[0]
    anomalie_label = id_to_label.get(anomalie_id, "inconnu")

    solution = clf_solution.predict([anomalie_label])[0]

    return {
        "status": "success",
        "values": {
            "pression": pression,
            "debit": debit,
            "humidite": humidite
        },
        "anomalie": anomalie_label,
        "solution": solution
    }
