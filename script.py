# import os
# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk
# from PIL import Image, ExifTags
# from rembg import remove
# import io

# class TraitementImages:
#     def __init__(self):
#         self.fenetre = tk.Tk()
#         self.fenetre.title("Breukh Console...")
#         self.fenetre.geometry("800x800")

#         self.dossier_entree = tk.StringVar()
#         self.dossier_sortie = tk.StringVar()

#         tk.Label(self.fenetre, text="Dossier d'entrée:").pack()
#         tk.Entry(self.fenetre, textvariable=self.dossier_entree, width=50).pack()
#         tk.Button(self.fenetre, text="Parcourir", command=self.choisir_dossier_entree).pack()

#         tk.Label(self.fenetre, text="Dossier de sortie:").pack()
#         tk.Entry(self.fenetre, textvariable=self.dossier_sortie, width=50).pack()
#         tk.Button(self.fenetre, text="Parcourir", command=self.choisir_dossier_sortie).pack()

#         self.select_all_var = tk.BooleanVar()
#         self.select_all_checkbox = tk.Checkbutton(self.fenetre, text="Sélectionner toutes les images", 
#                                                   variable=self.select_all_var, command=self.toggle_select_all)
#         self.select_all_checkbox.pack()

#         self.liste_images = ttk.Treeview(self.fenetre, columns=("Nom",), show="headings")
#         self.liste_images.heading("Nom", text="Nom de l'image")
#         self.liste_images.pack(pady=20, fill=tk.BOTH, expand=True)

#         self.progress_label = tk.Label(self.fenetre, text="")
#         self.progress_label.pack()

#         self.progress_bar = ttk.Progressbar(self.fenetre, orient="horizontal", length=300, mode="determinate")
#         self.progress_bar.pack(pady=10)

#         tk.Button(self.fenetre, text="Traiter les images sélectionnées", command=self.traiter_images).pack(pady=10)

#     def choisir_dossier_entree(self):
#         dossier = filedialog.askdirectory(title="Sélectionnez le dossier contenant les images à traiter")
#         if dossier:
#             self.dossier_entree.set(dossier)
#             self.charger_images()

#     def choisir_dossier_sortie(self):
#         dossier = filedialog.askdirectory(title="Sélectionnez le dossier de sortie")
#         if dossier:
#             self.dossier_sortie.set(dossier)

#     def charger_images(self):
#         dossier_entree = self.dossier_entree.get()
#         self.liste_images.delete(*self.liste_images.get_children())
#         fichiers = [f for f in os.listdir(dossier_entree) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
#         for fichier in fichiers:
#             self.liste_images.insert("", "end", values=(fichier,))
        
#         # Réinitialiser la case à cocher
#         self.select_all_var.set(False)

#     def toggle_select_all(self):
#         if self.select_all_var.get():
#             self.liste_images.selection_set(self.liste_images.get_children())
#         else:
#             self.liste_images.selection_remove(self.liste_images.get_children())

#     def traiter_images(self):
#         dossier_entree = self.dossier_entree.get()
#         dossier_sortie = self.dossier_sortie.get()

#         if not dossier_entree or not dossier_sortie:
#             messagebox.showerror("Erreur", "Veuillez sélectionner les dossiers d'entrée et de sortie.")
#             return

#         selections = self.liste_images.selection()
#         if not selections:
#             messagebox.showerror("Erreur", "Veuillez sélectionner au moins une image à traiter.")
#             return

#         total_images = len(selections)
#         self.progress_bar["maximum"] = total_images

#         for index, item in enumerate(selections, start=1):
#             fichier = self.liste_images.item(item, "values")[0]
#             chemin_entree = os.path.join(dossier_entree, fichier)
#             chemin_sortie = os.path.join(dossier_sortie, f"{os.path.splitext(fichier)[0]}.png")

#             self.progress_label.config(text=f"Traitement de l'image {index}/{total_images}: {fichier}")
#             self.fenetre.update()

#             with open(chemin_entree, 'rb') as file:
#                 img_data = file.read()

#             # Supprimer le fond
#             result = remove(img_data)
#             img = Image.open(io.BytesIO(result)).convert("RGBA")

#             # Appliquer la rotation EXIF si nécessaire
#             try:
#                 for orientation in ExifTags.TAGS.keys():
#                     if ExifTags.TAGS[orientation] == 'Orientation':
#                         break
#                 exif = dict(img._getexif().items())
#                 if orientation in exif:
#                     if exif[orientation] == 3:
#                         img = img.rotate(180, expand=True)
#                     elif exif[orientation] == 6:
#                         img = img.rotate(270, expand=True)
#                     elif exif[orientation] == 8:
#                         img = img.rotate(90, expand=True)
#             except (AttributeError, KeyError, IndexError):
#                 # Certaines images peuvent ne pas avoir de données EXIF
#                 pass

#             # Redimensionner l'image
#             img.thumbnail((800, 800), Image.LANCZOS)
            
#             # Créer une nouvelle image avec fond blanc de 800x800
#             nouvelle_img = Image.new('RGB', (800, 800), color=(255, 255, 255))
            
#             # Calculer la position pour centrer l'image
#             position = ((800 - img.width) // 2, (800 - img.height) // 2)
            
#             # Coller l'image redimensionnée sur le fond blanc
#             nouvelle_img.paste(img, position, img)
            
#             # Sauvegarder l'image traitée
#             nouvelle_img.save(chemin_sortie, format='PNG')

#             # Mettre à jour la barre de progression
#             self.progress_bar["value"] = index
#             self.fenetre.update()

#         self.progress_label.config(text=f"Terminé ! {total_images} image(s) traitée(s) avec succès.")
#         messagebox.showinfo("Terminé", f"{total_images} image(s) traitée(s) avec succès.")

#     def lancer(self):
#         self.fenetre.mainloop()

# if __name__ == "__main__":
#     app = TraitementImages()
#     app.lancer()


import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ExifTags, ImageEnhance
from rembg import remove, new_session
import io
import numpy as np
import cv2
import traceback
import sys
import logging

# Configuration du logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def exception_handler(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = exception_handler

class TraitementImages:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Breukh Console Améliorée Pro")
        self.fenetre.geometry("800x800")

        self.dossier_entree = tk.StringVar()
        self.dossier_sortie = tk.StringVar()

        tk.Label(self.fenetre, text="Dossier d'entrée:").pack()
        tk.Entry(self.fenetre, textvariable=self.dossier_entree, width=50).pack()
        tk.Button(self.fenetre, text="Parcourir", command=self.choisir_dossier_entree).pack()

        tk.Label(self.fenetre, text="Dossier de sortie:").pack()
        tk.Entry(self.fenetre, textvariable=self.dossier_sortie, width=50).pack()
        tk.Button(self.fenetre, text="Parcourir", command=self.choisir_dossier_sortie).pack()

        self.select_all_var = tk.BooleanVar()
        self.select_all_checkbox = tk.Checkbutton(self.fenetre, text="Sélectionner toutes les images", 
                                                  variable=self.select_all_var, command=self.toggle_select_all)
        self.select_all_checkbox.pack()

        self.liste_images = ttk.Treeview(self.fenetre, columns=("Nom",), show="headings")
        self.liste_images.heading("Nom", text="Nom de l'image")
        self.liste_images.pack(pady=20, fill=tk.BOTH, expand=True)

        self.progress_label = tk.Label(self.fenetre, text="")
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(self.fenetre, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

        tk.Button(self.fenetre, text="Traiter les images sélectionnées", command=self.traiter_images).pack(pady=10)

        self.log_text = tk.Text(self.fenetre, height=10)
        self.log_text.pack(pady=10)

        try:
            self.session = new_session("u2netp")  # Utilisation d'un modèle plus léger
            self.log("Session rembg initialisée avec succès.")
        except Exception as e:
            self.log(f"Erreur lors de l'initialisation de la session rembg: {str(e)}")
            logging.error(f"Erreur d'initialisation rembg: {str(e)}", exc_info=True)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.fenetre.update()
        logging.info(message)

    def choisir_dossier_entree(self):
        dossier = filedialog.askdirectory(title="Sélectionnez le dossier contenant les images à traiter")
        if dossier:
            self.dossier_entree.set(dossier)
            self.charger_images()

    def choisir_dossier_sortie(self):
        dossier = filedialog.askdirectory(title="Sélectionnez le dossier de sortie")
        if dossier:
            self.dossier_sortie.set(dossier)

    def charger_images(self):
        dossier_entree = self.dossier_entree.get()
        self.liste_images.delete(*self.liste_images.get_children())
        fichiers = [f for f in os.listdir(dossier_entree) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        for fichier in fichiers:
            self.liste_images.insert("", "end", values=(fichier,))
        self.select_all_var.set(False)

    def toggle_select_all(self):
        if self.select_all_var.get():
            self.liste_images.selection_set(self.liste_images.get_children())
        else:
            self.liste_images.selection_remove(self.liste_images.get_children())

    def pretraitement_image(self, img):
        try:
            self.log("Début du prétraitement")
            img_array = np.array(img)
            img_array = cv2.fastNlMeansDenoisingColored(img_array, None, 10, 10, 7, 21)
            lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl,a,b))
            img_array = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
            img = Image.fromarray(img_array)
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.5)
            self.log("Prétraitement terminé")
            return img
        except Exception as e:
            self.log(f"Erreur lors du prétraitement: {str(e)}")
            logging.error("Erreur de prétraitement", exc_info=True)
            return img

    def post_traitement_image(self, img):
        try:
            self.log("Début du post-traitement")
            img_array = np.array(img)
            r, g, b, a = cv2.split(img_array)
            a = cv2.medianBlur(a, 3)
            a = cv2.GaussianBlur(a, (3, 3), 0)
            a = cv2.normalize(a, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
            img_array = cv2.merge((r, g, b, a))
            self.log("Post-traitement terminé")
            return Image.fromarray(img_array)
        except Exception as e:
            self.log(f"Erreur lors du post-traitement: {str(e)}")
            logging.error("Erreur de post-traitement", exc_info=True)
            return img

    def traiter_images(self):
        try:
            dossier_entree = self.dossier_entree.get()
            dossier_sortie = self.dossier_sortie.get()

            if not dossier_entree or not dossier_sortie:
                messagebox.showerror("Erreur", "Veuillez sélectionner les dossiers d'entrée et de sortie.")
                return

            selections = self.liste_images.selection()
            if not selections:
                messagebox.showerror("Erreur", "Veuillez sélectionner au moins une image à traiter.")
                return

            total_images = len(selections)
            self.progress_bar["maximum"] = total_images

            for index, item in enumerate(selections, start=1):
                try:
                    fichier = self.liste_images.item(item, "values")[0]
                    chemin_entree = os.path.join(dossier_entree, fichier)
                    chemin_sortie = os.path.join(dossier_sortie, f"{os.path.splitext(fichier)[0]}.png")

                    self.progress_label.config(text=f"Traitement de l'image {index}/{total_images}: {fichier}")
                    self.log(f"Traitement de {fichier}")
                    self.fenetre.update()

                    self.log("Ouverture de l'image")
                    img = Image.open(chemin_entree)

                    # Appliquer la rotation EXIF ici, avant tout traitement
                    self.log("Application de la rotation EXIF")
                    try:
                        exif = img._getexif()
                        if exif:
                            orientation = exif.get(274, 1)  # 274 est le tag pour l'orientation
                            if orientation == 3:
                                img = img.rotate(180, expand=True)
                            elif orientation == 6:
                                img = img.rotate(270, expand=True)
                            elif orientation == 8:
                                img = img.rotate(90, expand=True)
                    except (AttributeError, KeyError, IndexError):
                        self.log("Pas de données EXIF pour la rotation")

                    img = img.convert("RGBA")

                    # Redimensionner l'image si elle est trop grande
                    max_size = 1500  # Ajustez cette valeur selon vos besoins
                    if img.width > max_size or img.height > max_size:
                        self.log(f"Redimensionnement de l'image (taille originale: {img.width}x{img.height})")
                        img.thumbnail((max_size, max_size), Image.LANCZOS)
                        self.log(f"Nouvelle taille: {img.width}x{img.height}")

                    img = self.pretraitement_image(img)

                    self.log("Conversion de l'image en bytes")
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()

                    self.log("Début de la suppression du fond")
                    try:
                        result = remove(img_byte_arr, session=self.session, alpha_matting=True, 
                                        alpha_matting_foreground_threshold=240, 
                                        alpha_matting_background_threshold=10,
                                        post_process_mask=True)
                        self.log("Suppression du fond terminée")
                    except Exception as e:
                        self.log(f"Erreur lors de la suppression du fond: {str(e)}")
                        logging.error("Erreur lors de la suppression du fond", exc_info=True)
                        continue  # Passer à l'image suivante en cas d'erreur
                    
                    img = Image.open(io.BytesIO(result)).convert("RGBA")
                    img = self.post_traitement_image(img)

                    self.log("Redimensionnement de l'image finale")
                    img.thumbnail((800, 800), Image.LANCZOS)
                    
                    # Création d'une nouvelle image avec fond blanc
                    nouvelle_img = Image.new('RGB', (800, 800), color=(255, 255, 255))
                    position = ((800 - img.width) // 2, (800 - img.height) // 2)
                    nouvelle_img.paste(img, position, img)

                    self.log("Sauvegarde de l'image")
                    nouvelle_img.save(chemin_sortie, format='PNG')

                    self.log(f"Image {fichier} traitée avec succès.")
                    self.progress_bar["value"] = index
                    self.fenetre.update()

                except Exception as e:
                    self.log(f"Erreur lors du traitement de {fichier}: {str(e)}")
                    logging.error(f"Erreur de traitement pour {fichier}", exc_info=True)

            self.progress_label.config(text=f"Terminé ! {total_images} image(s) traitée(s).")
            messagebox.showinfo("Terminé", f"{total_images} image(s) traitée(s).")
        except Exception as e:
            self.log(f"Erreur générale dans traiter_images: {str(e)}")
            logging.error("Erreur générale dans traiter_images", exc_info=True)

    def lancer(self):
        try:
            self.log("Démarrage de l'application...")
            self.fenetre.mainloop()
        except Exception as e:
            error_message = f"Erreur fatale : {str(e)}"
            print(error_message)
            logging.critical(error_message, exc_info=True)
            messagebox.showerror("Erreur Fatale", error_message)

if __name__ == "__main__":
    try:
        app = TraitementImages()
        app.lancer()
    except Exception as e:
        print(f"Erreur lors du lancement de l'application: {str(e)}")
        logging.critical("Erreur lors du lancement de l'application", exc_info=True)
        messagebox.showerror("Erreur de Lancement", str(e))