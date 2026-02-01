# audio_processor.py
import os
import subprocess

class AudioProcessor:
    def __init__(self, model_name="htdemucs", device="cpu"):
        """
        model_name: 'htdemucs' ou 'mdx_extra_q'
        device: 'cpu' ou 'cuda' si tu as GPU
        """
        self.model_name = model_name
        self.device = device
        self.separated_folder = "separated"

        # Crée le dossier séparé si il n'existe pas
        if not os.path.exists(self.separated_folder):
            os.makedirs(self.separated_folder)

    def separate(self, input_file):
        """
        Sépare les composantes audio d'un fichier.
        Retourne le dossier où les fichiers séparés sont stockés.
        """
        # Chemin absolu du fichier audio
        input_file = os.path.abspath(input_file)
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Le fichier '{input_file}' n'existe pas.")

        # Appelle Demucs via subprocess
        cmd = [
            "demucs",
            "-n", self.model_name,
            "-d", self.device,
            "-o", self.separated_folder,
            input_file
        ]

        print("Séparation en cours avec Demucs...")
        subprocess.run(cmd, check=True)

        # Récupère le dossier créé par Demucs
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        demucs_output_folder = os.path.join(self.separated_folder, self.model_name, base_name)

        if not os.path.exists(demucs_output_folder):
            raise FileNotFoundError(f"Dossier Demucs non trouvé : {demucs_output_folder}")

        print(f"Séparé dans : {demucs_output_folder}")
        return demucs_output_folder
