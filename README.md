Audio Separation Project – README
🎯 Objectif du projet
Ce projet permet de séparer automatiquement un fichier audio musical (ex : un morceau .mp3 ou .wav) en plusieurs pistes distinctes :
voix (vocals)
batterie (drums)
basse (bass)
autres instruments (other)
Il constitue la première brique d’un projet plus large visant, à terme, la création de partitions musicales à partir de fichiers audio.
🧠 Choix technologiques
Pourquoi Demucs ?
Demucs est actuellement l’un des meilleurs modèles open-source de séparation musicale :
✅ Très haute qualité de séparation
✅ Fonctionne sur CPU (pas besoin de GPU)
✅ Facilement utilisable via la ligne de commande
✅ Stable et éprouvé en production
Pourquoi utiliser Demucs via subprocess ?
Le projet utilise Demucs via sa CLI (ligne de commande) et non via son API Python interne.
Raisons principales :
❌ L’API Python interne de Demucs change souvent
❌ Nombreuses erreurs rencontrées :
apply_model
torchcodec
ffmpeg
✅ La CLI Demucs est stable, robuste et fiable
✅ Aucun couplage avec l’implémentation interne du modèle
👉 Ce choix garantit un projet maintenable, portable et robuste, notamment sous Linux.
🏗️ Architecture du projet
Le projet repose volontairement sur deux fichiers Python seulement :
my_audio_app/
│
├── main_app.py          # Interface utilisateur / point d’entrée
├── audio_processor.py   # Logique métier : séparation audio
Principe fondamental
main_app.py → ce que l’utilisateur lance
audio_processor.py → ce que l’application fait réellement
Cette séparation permet :
de changer l’interface plus tard (CLI → GUI → Web)
de garder un moteur audio propre et réutilisable
⚙️ audio_processor.py – Le cœur du projet
Rôle
Ce fichier contient toute la logique audio.
Il :
vérifie que le fichier audio existe
appelle Demucs
récupère les pistes séparées
retourne le dossier de sortie
Fonctionnement détaillé
Initialisation
class AudioProcessor:
    def __init__(self, model_name="htdemucs", device="cpu"):
model_name : modèle Demucs utilisé (htdemucs par défaut)
device : cpu ou cuda (CPU recommandé pour la stabilité)
Lors de l’initialisation, un dossier separated/ est créé automatiquement s’il n’existe pas.
Séparation audio
def separate_and_clean(self, input_file):
⚠️ Malgré son nom, aucun nettoyage audio n’est effectué dans la version actuelle.
Ce choix est volontaire :
éviter une consommation disque inutile
garder une base stable et simple
Appel à Demucs (point clé)
cmd = [
    "demucs",
    "-n", self.model_name,
    "-d", self.device,
    "-o", self.separated_folder,
    input_file
]
Demucs est appelé exactement comme en ligne de commande, équivalent à :
demucs -n htdemucs -d cpu -o separated mon_fichier.mp3
Avantages
✅ Aucun problème de version Python
✅ Aucune dépendance à l’API interne de Demucs
✅ Très robuste sur Linux
Résultat généré
Demucs crée automatiquement la structure suivante :
separated/
└── htdemucs/
    └── nom_du_morceau/
        ├── vocals.wav
        ├── drums.wav
        ├── bass.wav
        └── other.wav
👉 Le chemin de ce dossier est retourné à l’application.
▶️ main_app.py – Point d’entrée utilisateur
Rôle
main_app.py agit comme contrôleur :
instancie AudioProcessor
lance la séparation audio
affiche les messages à l’utilisateur
👉 C’est le fichier à exécuter.
Exemple de logique
processor = AudioProcessor()
output = processor.separate_and_clean("ya.mp3")
Cela suffit à :
lancer Demucs
séparer le morceau
récupérer les pistes audio
🐧 Installation sous Linux (à partir de zéro)
1️⃣ Prérequis système
sudo apt update
sudo apt install -y python3 python3-venv ffmpeg
⚠️ FFmpeg est obligatoire pour Demucs.
2️⃣ Création de l’environnement Python
python3 -m venv audio-ai
source audio-ai/bin/activate
3️⃣ Installation des dépendances
pip install --upgrade pip
pip install demucs
Aucune autre dépendance n’est nécessaire pour la séparation audio.
4️⃣ Lancer l’application
Place un fichier audio dans le dossier du projet, puis :
python main_app.py
Ou directement :
python -c "
from audio_processor import AudioProcessor
p = AudioProcessor()
p.separate_and_clean('mon_morceau.mp3')
"
📦 Sortie du programme
Le programme retourne le dossier contenant les pistes séparées, prêt à être utilisé pour :
écoute individuelle
traitement ultérieur
transcription musicale (étape future du projet)
Si tu veux, je peux maintenant :
ajouter une section “Future work – Partition musicale”
ou adapter ce README pour un rendu universitaire / startup / GitHub public
