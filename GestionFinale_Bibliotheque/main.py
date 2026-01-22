
import tkinter as tk
import sys
import os
from pathlib import Path

# Ajouter le répertoire courant au chemin Python
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

from app import BibliothequApp

def main():
    """
    Fonction principale.
    Initialise et lance l'application.
    """
    # Créer la fenêtre racine
    root = tk.Tk()
    
    # Définir l'icône si disponible
    try:
        # Vous pouvez remplacer ceci par un vrai chemin d'icône
        # root.iconbitmap("assets/icon.ico")
        pass
    except Exception as e:
        print(f"Avertissement: Icône non trouvée: {e}")
    
    # Initialiser l'application
    app = BibliothequApp(root)
    
    # Lancer la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()
