# CV_Formater

Application permettant de formater des CV pour l'entreprise Antares. Cette version est conçue uniquement pour une utilisation sur Linux (Ubuntu).

## Mode d'emploi de l'installation de l'application :

### Prérequis :

Pour installer l'application
- il faut avoir les droits administrateur sur la session sur laquelle on se trouve 
- avoir un compte MistralAI : 
- https://console.mistral.ai/ : puis aller sur API (pour créditer aller dans "Facturation" puis ajouter des fonds) 
- SI vous avez déjà un compte, vous pouvez créer une nouvelle clé secrete, via ce lien : https://console.mistral.ai/api-keys/
- Une fois la clée obtenue la stocker quelque part car on ne la voit qu'une seule fois  

Déroulement de l'installation : 

### Étape 1 : Ouvrir l'invite de commande 

Aller dans afficher les applications, puis lancer l'application 'Terminal'.

### Étape 2 :

Entrer la commande suivante : elle installe Python !

sudo apt update
sudo apt install python3
sudo apt install python3-pip

### Étape 3 : valide les phases 

Une fois l'installation terminée, entrez la commande suivante pour vérifier la bonne installation de Python :

python --version

### Étape 4 : Installation des bibliothètques 

Entrer les commandes suivantes d'un coup, telle que présentés ci-dessous : 

pip install numpy
pip install kivy
pip install python-docx
pip install python-dateutil
pip install python-dotenv
pip install mistralai

### Étape 5 :

Aller maintenant dans l'équipe Teams où se trouve le dossier CV_FormaterMistal_Linux, puis téléchargez-le. Ouvrez votre téléchargement, faites "Extraire" et choisissez le répertoire où vous voulez placer le dossier.

### Étape 6 :

Pour lancer l'application, dans le terminal vous aller dans le répertoire ou vous avez extrait votre dossier. Imaginons que vous l'ayez extrait dans "Documents" alors entrer la commande suivante :

cd home/<nom d'utilisteur de la session>/Documents/CV_Formater_Mistral_Linux

Si vous ne connaisser pas le chemin pour accéder avotre fichier, entrer la commande suivante :

find / -name "CV_Formater_Mistral_Linux" 2>/dev/null

Puis entrer la commande suivante : 

python3 main.py (ou encore : sudo python3 main.py)

---------------------------------------------------------------------------------

## Guide d'utilisation de l'application

- Tout d'abord, coller votre clé API que vous avez créé précedemment dans l'espace dédier et cliquer sur "Sauvegarder la clé API" (Cliquer sur "Sauvegarder la clé API" à chaque fois que vous voulez formater un CV)
- Maintenant récupérer le CV qu'on souhaite formater. Copier le contenu et le coller dans l'interface du programme CV_Formater. 
- Choisissez ensuite le dossier où vous allez enregistrer le fichier ainsi que son nom (il n'est pas nécessaire de préciser l'extension, le fichier sera automatiquement un fichier .docx). 
Attendez quelques secondes le temps de la génération du fichier, puis un message indiquera que le fichier a bien été généré et où il se trouve dans le répertoire de l'appareil. 
L'opération est répétable plusieurs fois. 
Attention au DC trop volumineaux, dans ce cas, il faut le faire en 2,3 voir 4 fois. Par exmeple un CV de 8 pages à minima en 2 fois, 12/14 pages, 3 fois ...
Fin du processus : 
- Le nom du profil + Titre ne sont pas mis à jour, il faut le faire manuellement. 
- Attention tout de même aux dates notamment, il faut les vérifier au cas où il y ait des erreurs.
- Il se peut qu'il se trouve des erreurs, ce modèle n'est qu'une première version, toute récente et donc est loin d'être parfaite.


## Comment cette application a été mise en œuvre

Pour créer cette application de formatage de CV au format de l'entreprise Antares, nous avons pris avantage de l'IA pour rendre le processus rapide et simple. Dans un premier temps, le texte que l'utilisateur va entrer est celui qui se trouve dans le CV à formater. Ensuite, trois requêtes sont envoyées à ChatGPT via son API : une pour les formations du candidat, une pour les compétences, et une dernière pour ses expériences professionnelles. L'objectif est qu'à l'issue de ces requêtes, l'IA retourne des tableaux Python où les informations du candidat sont spécifiquement organisées pour pouvoir être utilisées dans le script qui crée le fichier .docx. Ce script crée le template de l'entreprise, puis prend les tableaux et place les informations dans le fichier grâce à des boucles `for`. Pour que l'IA puisse bien créer ces tableaux, il a fallu lui donner des exemples de tableaux Python dans les prompts. Enfin, nous utilisons Kivy pour créer l'interface utilisateur.


