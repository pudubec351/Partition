# main_app.py
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel
)
from audio_processor import AudioProcessor

class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Séparation Audio avec Demucs")
        self.setGeometry(100, 100, 400, 200)

        self.processor = AudioProcessor()
        self.file_path = None

        # Widgets
        self.label = QLabel("Aucun fichier sélectionné", self)
        self.select_btn = QPushButton("Choisir un fichier audio", self)
        self.process_btn = QPushButton("Séparer audio", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.select_btn)
        layout.addWidget(self.process_btn)
        self.setLayout(layout)

        # Connexions
        self.select_btn.clicked.connect(self.select_file)
        self.process_btn.clicked.connect(self.process_file)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Sélectionner un fichier audio", "", "Audio Files (*.mp3 *.wav *.flac)"
        )
        if file_path:
            self.file_path = file_path
            self.label.setText(f"Fichier sélectionné : {os.path.basename(file_path)}")

    def process_file(self):
        if not self.file_path:
            self.label.setText("Veuillez sélectionner un fichier d'abord !")
            return
        try:
            output_folder = self.processor.separate(self.file_path)
            self.label.setText(f"Séparation terminée dans : {output_folder}")
        except Exception as e:
            self.label.setText(f"Erreur : {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioApp()
    window.show()
    sys.exit(app.exec())


