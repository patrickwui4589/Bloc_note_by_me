import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import Menu, Toplevel

class BlocNotes:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloc-notes amélioré")

        # Zone de texte
        self.text_area = tk.Text(root, undo=True)
        self.text_area.pack(expand=True, fill="both")

        # Barre de menu
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)

        # Menu Fichier
        fichier_menu = Menu(self.menu_bar, tearoff=0)
        fichier_menu.add_command(label="Ouvrir", command=self.ouvrir_fichier)
        fichier_menu.add_command(label="Sauvegarder", command=self.sauvegarder_fichier)
        fichier_menu.add_separator()
        fichier_menu.add_command(label="Quitter", command=self.quitter)
        self.menu_bar.add_cascade(label="Fichier", menu=fichier_menu)

        # Menu Édition
        edition_menu = Menu(self.menu_bar, tearoff=0)
        edition_menu.add_command(label="Couper", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edition_menu.add_command(label="Copier", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edition_menu.add_command(label="Coller", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edition_menu.add_separator()
        edition_menu.add_command(label="Rechercher", command=self.rechercher_mot)
        self.menu_bar.add_cascade(label="Édition", menu=edition_menu)

    def ouvrir_fichier(self):
        chemin = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        if chemin:
            with open(chemin, "r", encoding="utf-8") as fichier:
                contenu = fichier.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, contenu)

    def sauvegarder_fichier(self):
        chemin = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
        if chemin:
            with open(chemin, "w", encoding="utf-8") as fichier:
                contenu = self.text_area.get(1.0, tk.END)
                fichier.write(contenu)

    def quitter(self):
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter ?"):
            self.root.quit()

    def rechercher_mot(self):
        fenetre = Toplevel(self.root)
        fenetre.title("Rechercher un mot")
        fenetre.geometry("300x100")

        tk.Label(fenetre, text="Mot à rechercher :").pack(pady=5)
        entree_mot = tk.Entry(fenetre)
        entree_mot.pack()

        def surligner():
            mot = entree_mot.get()
            self.text_area.tag_remove('highlight', '1.0', tk.END)
            if mot:
                index = '1.0'
                while True:
                    index = self.text_area.search(index, nocase=1, stopindex=tk.END)
                    if not index:
                        break
                    fin_index = f"{index}+{len(mot)}c"
                    self.text_area.tag_add('highlight', index, fin_index)
                    index = fin_index
                self.text_area.tag_config('highlight', background='yellow', foreground='black')

        tk.Button(fenetre, text="Rechercher", command=surligner).pack(pady=5)

# Lancer l'application
if __name__ == "__main__":
    racine = tk.Tk()
    app = BlocNotes(racine)
    racine.mainloop()
