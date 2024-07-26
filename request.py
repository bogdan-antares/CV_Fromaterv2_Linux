import os
import re
import subprocess
import sys
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise EnvironmentError("La clé API Mistral n'est pas définie. Veuillez définir la variable d'environnement 'MISTRAL_API_KEY'.")

model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

exemple1 = """
# Ajouter des entrées de formation, le tableau formations doit s'appeler "formations". Ne change pas le nom je te rappelle que ce que tu retournes sera directement inclus dans un code python et donc il faut respecter la structure. Evite les erreurs suivantes

    for char in text:
TypeError: 'int' object is not iterable


    for year, descriptions in trainings:
ValueError: too many values to unpack (expected 2) :

formations = [
    ("2023", "Certificat de compétence Analyste en Cybersécurité, CNAM / Cours à Distance"),
    ("2012", "BTS Informatique de Gestion (niveau), Lycée Saint Paul Bourdon Blanc, Orléans"),
    ("2010", "BAC Pro, Micro-Informatique, Installation et maintenance, Lycée Saint Paul Bourdon Blanc, Orléans"),
    ("2008", "BAC Technologique STI Génie Electronique, Lycée Maurice Genevoix, Ingé, France")
]
"""

exemple2 = """
# Ajouter des compétences et sous-compétences, le tableau competences doit s'appeler 'competences'. Ne change pas le nom je te rappelle que ce que tu retournes sera directement inclus dans un code python et donc il faut respecter la structure :
competences = {
    "Logiciels & Compétences": [
        "Support utilisateurs",
        "Active directory (classique)",
        "Déploiement",
        "Pack Office 2013, 19, 365",
        "Gestion de parc SI",
        "Sécurité informatique"
    ],
    "Langues": [
        "Français : Bilingue",
        "Espagnol : Compétences professionnelles"
    ]
}
"""

exemple3 = """
# Ajouter des expériences professionnelles, le tableau experience doit s'appeler "experiences". Ne change pas le nom je te rappelle que ce que tu retournes sera directement inclus dans un code python et donc il faut respecter la structure et éviter d'avoir ces erreurs :

entreprise, periode, poste, description, technologies = experience
ValueError: not enough values to unpack (expected 5, got 4)

    desc_run = desc_paragraph.runs[0]
IndexError: list index out of range :

experiences = [
    ("ORCOM", "Depuis 2020 – Orléans", "Technicien de support Informatique",
     [
         "Commande, déploiement, gestion de stock, attributions des matériels informatiques et au besoin retour garantie (DELL).",
         "Mise à jour des applications métiers serveur et utilisateurs.",
         "Création utilisateurs (Active directory, exchange, office 365, ouverture accès application métier, gestion de droits).",
         "Gestion des demandes et des incidents utilisateurs (modification droits, accès aux applications après validation).",
         "Déplacements sur site distant si besoin.",
         "Gestion de la plateforme de filtrage de mail.",
         "Gestion des incidents de niveau 1, 2 et 3 en support des administrateurs réseau si besoin."
     ], ["Active Directory", "Exchange", "Office 365"]),
    ("SERVIER", "Mai 2020 - Août 2020 – Orléans", "Technicien de déploiement",
     [
         "Déploiement de postes neufs sous Windows 10, installation application métier et livraison à l’utilisateur final après prise de rendez-vous.",
         "Gestion des incidents et des problématiques après livraison du poste à l’utilisateur final."
     ], ["Windows 10"]),
    ("Conseil Régional Du Centre", "Mai 2019 - Août 2019 et Décembre 2019 – Orléans", "Technicien support de Niveau 2",
     [
         "Installation et paramétrage de nouveaux matériels.",
         "Gestion des incidents de niveau 2, prise en main à distance ou déplacement auprès des collaborateurs."
     ], []),
    ("Siemens, Banques CIC, Valloire Habitat", "Septembre 2019 - Novembre 2019 – Région Centre", "Technicien de déploiement",
     [
         "Paramétrage smartphone, déploiement applications et livraison utilisateur final.",
         "Déploiement image et paramétrage applications."
     ], ["Smartphone Configuration", "Application Deployment"]),
    ("Adecco, Proman, Smathpeople, etc.", "2012 - 2019 – Région Centre", "Technicien IT",
     [
         "Différentes missions intérim dans des domaines variés."
     ], [])
]
"""

def send_to_mistral(prompt):
    try:
        messages = [ChatMessage(role="user", content=prompt)]
        chat_response = client.chat(model=model, messages=messages)
        return chat_response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erreur lors de l'envoi de la requête à Mistral : {e}")
        return None

def main(cv_test_file, save_path):
    with open(cv_test_file, 'r', encoding='utf-8') as file:
        cv_text = file.read()

    tab_py = [exemple1, exemple2, exemple3]
    tab_titres = ["formation", "compétences", "expériences professionnels"]
    final_text = ""

    for compt, titre in enumerate(tab_titres):
        prompt = f"""
        Voici le contenu d'un CV :

        {cv_text}

        Veuillez trier les informations de {titre} et les formater en structures de données Python comme ci-dessous, donc servez vous de l'exemple ci-dessous pour formater les données de {titre} du texte ci-dessus issue d'un CV :

        {tab_py[compt]}

        Dans ta réponse, répond seulement avec du code python, si tu veux rajouter un texte tu mets un '#' sinon tu ne réponds uniquement qu'avec du code python car ta réponse sera directement enregistrée dans un code python. Pense à bien respecter la structure des tableaux. Si par exemple il manque une année dans les formations, mets des accolades vides à cet endroit. Pense aussi à respecter le nom du tableau de l'exemple et le même que celui où tu vas stocker les données.
        """
        sorted_info = send_to_mistral(prompt)
        if sorted_info is not None:
            lines = sorted_info.split('\n')
            cleaned_info = '\n'.join(line for line in lines if "```" not in line)
            final_text += cleaned_info + '\n'
        else:
            print("Erreur lors de la récupération des données auprès de Mistral.")

    if final_text:
        with open('data.py', 'w', encoding='utf-8') as f:
            f.write(final_text)
    else:
        print("Aucune donnée à écrire dans data.py.")
        sys.exit(1)

    try:
        result = subprocess.run([sys.executable, 'template.py', save_path], check=True, capture_output=True, text=True)
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        print(f"Output: {e.stdout}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python request.py <cv_text_file> <save_path>")
        sys.exit(1)

    cv_text_file = sys.argv[1]
    save_path = sys.argv[2]

    main(cv_text_file, save_path)


