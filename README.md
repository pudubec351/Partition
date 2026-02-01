# Partition

Choix technologiques
Pourquoi Demucs ?
Demucs est actuellement l’un des meilleurs modèles open-source de séparation musicale :
Très bonne qualité
Fonctionne sur CPU (pas besoin de GPU)
Facile à intégrer via la ligne de commande

utiliser Demucs via subprocess, plutôt que via son API Python interne.

Pourquoi ?
L’API interne change souvent
Beaucoup d’erreurs (apply_model, torchcodec, ffmpeg, etc.)
La CLI Demucs est stable, robuste et production-ready

Architecture du projet
Le projet repose volontairement sur deux fichiers Python seulement :
my_audio_app/
│
├── main_app.py          # Interface utilisateur / point d’entrée
├── audio_processor.py   # Logique métier : séparation audio
Principe fondamental
main_app.py = “ce que l’utilisateur voit”
audio_processor.py = “ce que l’application fait réellement”
Cette séparation permet :
De remplacer plus tard l’interface (CLI → GUI → Web)
De garder un moteur audio propre et réutilisable

audio_processor.py – Le cœur du projet
Rôle
Ce fichier contient toute la logique audio.
Il :
Vérifie que le fichier audio existe
Appelle Demucs
Récupère les pistes séparées




audio_processor.py – Le cœur du projet
Rôle
Ce fichier contient toute la logique audio.
Il :
Vérifie que le fichier audio existe
Appelle Demucs
Récupère les pistes séparées
Retourne le dossier de sortie
Fonctionnement détaillé
Initialisation
class AudioProcessor:
    def __init__(self, model_name="htdemucs", device="cpu"):
model_name : modèle Demucs utilisé (htdemucs par défaut)
device : CPU ou GPU (cpu est le choix le plus stable)
Un dossier separated/ est créé automatiquement pour stocker les résultats.
Séparation audio
def separate_and_clean(self, input_file):
Même si le nom contient clean, dans la version actuelle il n’y a PAS de nettoyage audio.
Ce choix est volontaire pour :
éviter une consommation disque excessive
garder une base stable
Appel à Demucs (point clé)
cmd = [
    "demucs",
    "-n", self.model_name,
    "-d", self.device,
    "-o", self.separated_folder,
    input_file
]
👉 Demucs est appelé comme en ligne de commande, exactement comme si l’utilisateur tapait :
demucs -n htdemucs -d cpu -o separated mon_fichier.mp3
Avantage :
Aucun problème de version Python
Aucune dépendance interne à Demucs
Très robuste sur Linux
Résultat
Demucs crée automatiquement une structure :
separated/
└── htdemucs/
    └── nom_du_morceau/
        ├── vocals.wav
        ├── drums.wav
        ├── bass.wav
        └── other.wav
Ce dossier est retourné à l’application.
5. main_app.py – Le point d’entrée utilisateur
Rôle
main_app.py sert de contrôleur :
Il appelle AudioProcessor
Il lance la séparation
Il affiche les messages à l’utilisateur
👉 C’est ce fichier que l’on exécute.
Exemple de logique
processor = AudioProcessor()
output = processor.separate_and_clean("ya.mp3")
Cela suffit à :
lancer Demucs
séparer le morceau
récupérer les pistes audio
6. Installation sous Linux (à partir de zéro)
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
Place un fichier audio dans le dossier, puis :
python main_app.py
ou en direct :
python -c "
from audio_processor import AudioProcessor
p = AudioProcessor()
p.separate_and_clean('mon_morceau.mp3')

Retourne le dossier de sortie
