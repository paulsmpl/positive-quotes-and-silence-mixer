import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import random
from tqdm import tqdm

# Fonction pour générer un fichier audio de bruit blanc
def generer_bruit_blanc(duree):
    return AudioSegment.silent(duration=duree)

# Fonction pour créer le mélange audio
def creer_melange():
    # Charger les fichiers audio originaux
    fichiers_audio_originaux = []
    for chemin in chemins_fichiers_audio_originaux:
        fichier_audio_original = AudioSegment.from_file(chemin)
        fichiers_audio_originaux.append(fichier_audio_original)

    # Charger le fichier audio de bruit blanc
    bruit_blanc = AudioSegment.from_file(chemin_fichier_bruit_blanc)

    # Durée totale du mélange
    duree_totale = int(entry_duree_totale.get()) * 60 * 1000  # Convertir en millisecondes

    # Créer une piste vide pour le mélange
    melange = AudioSegment.silent(duration=duree_totale)

    # Superposer les fichiers audio originaux sur le bruit blanc de manière aléatoire
    position_actuelle = 0
    pourcentage_fichiers_audio = float(entry_pourcentage_fichiers_audio.get())
    pourcentage_bruit_blanc = 100 - pourcentage_fichiers_audio
    with tqdm(total=duree_totale, desc="Création du mélange audio") as pbar:
        while position_actuelle < duree_totale:
            # Choix aléatoire entre fichier audio original et bruit blanc
            if random.random() < pourcentage_fichiers_audio / 100:
                # Sélection aléatoire d'un fichier audio original
                fichier_audio_original = random.choice(fichiers_audio_originaux)
                melange = melange.overlay(fichier_audio_original, position=position_actuelle)
                position_actuelle += len(fichier_audio_original)
            else:
                # Ajouter du bruit blanc
                duree_bruit_blanc = random.randint(3000, 3000)  # Durée du bruit blanc entre 0.1 et 1 seconde
                melange = melange.overlay(generer_bruit_blanc(duree_bruit_blanc), position=position_actuelle)
                position_actuelle += duree_bruit_blanc
            pbar.update(min(len(fichier_audio_original), duree_bruit_blanc))

    # Écrire le fichier audio résultant
    melange.export("melange_final.mp3", format="mp3")
    print("Mélange audio créé avec succès !")

# Fonction pour sélectionner les fichiers audio originaux
def selectionner_fichiers_audio_originaux():
    global chemins_fichiers_audio_originaux
    chemins_fichiers_audio_originaux = filedialog.askopenfilenames()
    label_fichiers_audio_originaux.config(text="Fichiers audio originaux sélectionnés : " + ", ".join(chemins_fichiers_audio_originaux))

# Fonction pour sélectionner le fichier audio de bruit blanc
def selectionner_fichier_bruit_blanc():
    global chemin_fichier_bruit_blanc
    chemin_fichier_bruit_blanc = filedialog.askopenfilename()
    label_fichier_bruit_blanc.config(text="Fichier audio de bruit blanc sélectionné : " + chemin_fichier_bruit_blanc)

# Créer la fenêtre principale
root = tk.Tk()
root.title("Création de mélange audio")

# Champ d'entrée pour spécifier le pourcentage de fichiers audio originaux
label_pourcentage_fichiers_audio = tk.Label(root, text="Pourcentage de fichiers audio originaux:")
label_pourcentage_fichiers_audio.pack(pady=5)
entry_pourcentage_fichiers_audio = tk.Entry(root)
entry_pourcentage_fichiers_audio.insert(0, "20")  # Valeur par défaut
entry_pourcentage_fichiers_audio.pack(pady=5)

# Champ d'entrée pour spécifier la durée totale du mélange (en minutes)
label_duree_totale = tk.Label(root, text="Durée totale du mélange (en minutes):")
label_duree_totale.pack(pady=5)
entry_duree_totale = tk.Entry(root)
entry_duree_totale.insert(0, "60")  # Valeur par défaut
entry_duree_totale.pack(pady=5)

# Bouton pour sélectionner les fichiers audio originaux
btn_selectionner_fichiers_audio_originaux = tk.Button(root, text="Sélectionner les fichiers audio originaux", command=selectionner_fichiers_audio_originaux)
btn_selectionner_fichiers_audio_originaux.pack(pady=10)

# Étiquette pour afficher les fichiers audio originaux sélectionnés
label_fichiers_audio_originaux = tk.Label(root, text="")
label_fichiers_audio_originaux.pack()

# Bouton pour sélectionner le fichier audio de bruit blanc
btn_selectionner_fichier_bruit_blanc = tk.Button(root, text="Sélectionner le fichier audio de bruit blanc", command=selectionner_fichier_bruit_blanc)
btn_selectionner_fichier_bruit_blanc.pack(pady=10)

# Étiquette pour afficher le fichier audio de bruit blanc sélectionné
label_fichier_bruit_blanc = tk.Label(root, text="")
label_fichier_bruit_blanc.pack()

# Bouton pour créer le mélange audio
btn_creer_melange = tk.Button(root, text="Créer le mélange audio", command=creer_melange)
btn_creer_melange.pack(pady=20)

# Lancer l'interface utilisateur
root.mainloop()
