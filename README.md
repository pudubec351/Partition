# 🎵 Audio Separation Project

Séparation automatique de morceaux musicaux en pistes individuelles  
(voix, batterie, basse, autres instruments) à l’aide de **Demucs**.

---

## 🎯 Objectif du projet

Ce projet permet de **séparer un fichier audio musical** (`.mp3`, `.wav`, etc.) en plusieurs pistes distinctes :

- 🎤 **Vocals** (voix)
- 🥁 **Drums** (batterie)
- 🎸 **Bass** (basse)
- 🎹 **Other** (autres instruments)

Il constitue la **première brique d’un projet plus large** visant, à terme, la **génération de partitions musicales** à partir d’un fichier audio.

---

## 🧠 Choix technologiques

### Pourquoi Demucs ?

**Demucs** est aujourd’hui l’un des meilleurs modèles open-source de séparation musicale :

- ✅ Excellente qualité de séparation
- ✅ Fonctionne sur **CPU** (pas besoin de GPU)
- ✅ Utilisable facilement via la **ligne de commande**
- ✅ Stable et éprouvé en production

---

### Pourquoi utiliser Demucs via `subprocess` ?

Ce projet utilise **Demucs via sa CLI** (ligne de commande), et **pas via son API Python interne**.

#### Raisons principales :

- ❌ L’API Python interne de Demucs change fréquemment
- ❌ Nombreuses erreurs rencontrées :
  - `apply_model`
  - `torchcodec`
  - `ffmpeg`
- ✅ La CLI Demucs est **stable, robuste et fiable**
- ✅ Aucun couplage avec l’implémentation interne du modèle

👉 Ce choix garantit un projet **maintenable, portable et robuste**, notamment sous Linux.

---

## 🏗️ Architecture du projet

Le projet repose volontairement sur **deux fichiers Python seulement** :

my_audio_app/
├── main_app.py # Point d’entrée / interface utilisateur
└── audio_processor.py # Logique métier : séparation audio

### Principe fondamental

- `main_app.py` → **ce que l’utilisateur lance**
- `audio_processor.py` → **ce que l’application fait réellement**

Cette séparation permet :

- 🔁 de changer l’interface plus tard (CLI → GUI → Web)
- 🧠 de garder un moteur audio propre et réutilisable

---

## ⚙️ audio_processor.py — Le cœur du projet

### Rôle

Ce fichier contient **toute la logique audio**. Il :

- vérifie que le fichier audio existe
- appelle Demucs
- récupère les pistes séparées
- retourne le dossier de sortie

---

### Fonctionnement détaillé

## 🐧 Installation (Linux)

Cette section explique comment installer et lancer le projet **à partir de zéro** sur une machine Linux.

---

### 1️⃣ Prérequis système

Assure-toi d’avoir les paquets suivants installés :

```bash
sudo apt update
sudo apt install -y python3 python3-venv ffmpeg
ℹ️ FFmpeg est obligatoire : Demucs l’utilise pour lire et convertir les fichiers audio.
2️⃣ Création de l’environnement Python
Depuis le dossier du projet :
python3 -m venv audio-ai
source audio-ai/bin/activate
Une fois activé, ton terminal doit afficher quelque chose comme :
(audio-ai) user@machine:~$
3️⃣ Installation des dépendances Python
Mets à jour pip, puis installe Demucs :
pip install --upgrade pip
pip install demucs
✅ Aucune autre dépendance n’est nécessaire pour la séparation audio.
4️⃣ Lancer l’application
Place un fichier audio (.mp3, .wav, etc.) dans le dossier du projet, puis lance :
python main_app.py
Ou directement depuis Python :
python -c "
from audio_processor import AudioProcessor
p = AudioProcessor()
p.separate_and_clean('mon_morceau.mp3')
"
5️⃣ Résultat
Les pistes séparées sont générées dans le dossier :
separated/
Chaque morceau contient ses pistes individuelles (vocals, drums, bass, other),
prêtes à être utilisées

