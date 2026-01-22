
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from database import LibraryDatabase

class BibliothequApp:
  

    COULEUR_SIDEBAR = "#1A252F"          
    COULEUR_PRIMAIRE = "#2C3E50"          
    COULEUR_SECONDAIRE = "#3498DB"        
    COULEUR_ACCENT = "#E74C3C"            
    COULEUR_SUCCES = "#27AE60"            
    COULEUR_FOND = "#ECF0F1"              
    COULEUR_TEXTE = "#2C3E50"             
    COULEUR_TEXTE_CLAIR = "#FFFFFF"       
    COULEUR_BOUTON_HOVER = "#34495E"      
    
    def __init__(self, root):
        """
        Initialise l'application principale.
        
        Args:
            root: Fenêtre Tkinter racine
        """
        self.root = root
        self.root.title("Gestion de Bibliothèque")
        self.root.geometry("1400x750")
        self.root.resizable(True, True)
        self.root.configure(bg=self.COULEUR_FOND)
        
        # Initialiser la base de données
        self.db = LibraryDatabase()
        
        # Variable pour stocker le livre actuellement édité
        self.current_book_id = None
        self.current_image_path = None
        self.current_page = None
        
        # Configurer les styles
        self._configure_styles()
        
        # Créer la structure principale: sidebar + content
        self._create_layout()
        
        # Afficher le dashboard au démarrage
        self.show_dashboard()
    
    def _configure_styles(self):
        """Configure les styles Tkinter avec couleurs modernes."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style pour les boutons
        style.configure(
            'Accent.TButton',
            font=('Segoe UI', 10, 'bold'),
            padding=10,
            background=self.COULEUR_SECONDAIRE,
            foreground=self.COULEUR_TEXTE_CLAIR
        )
        
        style.configure(
            'Danger.TButton',
            font=('Segoe UI', 10, 'bold'),
            padding=10,
            background=self.COULEUR_ACCENT
        )
        
        style.configure(
            'Success.TButton',
            font=('Segoe UI', 10, 'bold'),
            padding=10,
            background=self.COULEUR_SUCCES
        )
    
    def show_frame(self, cont):
        """
        Affiche une page spécifique.
        
        Args:
            cont: Classe de la page à afficher
        """
        frame = self.frames[cont]
        frame.tkraise()
        frame.refresh()
    
    def create_button(self, parent, text, command, style="Accent.TButton", width=20):
        """
        Crée un bouton stylisé.
        
        Args:
            parent: Widget parent
            text: Texte du bouton
            command: Fonction à exécuter
            style: Style du bouton
            width: Largeur du bouton
            
        Returns:
            Bouton créé
        """
        btn = ttk.Button(
            parent,
            text=text,
            command=command,
            style=style,
            width=width
        )
        return btn
    
    def create_label(self, parent, text, font_size=12, font_weight="normal", fg=None):
        """
        Crée un label stylisé.
        
        Args:
            parent: Widget parent
            text: Texte du label
            font_size: Taille de la police
            font_weight: Poids de la police
            fg: Couleur du texte
            
        Returns:
            Label créé
        """
        if fg is None:
            fg = self.COULEUR_TEXTE
        
        label = tk.Label(
            parent,
            text=text,
            font=('Segoe UI', font_size, font_weight),
            bg=self.COULEUR_FOND,
            fg=fg
        )
        return label


    def _configure_styles(self):
        """Configure les styles Tkinter avec couleurs modernes."""
        style = ttk.Style()
        style.theme_use('clam')
    
    def _create_layout(self):
        """Crée la structure principale avec sidebar et content area."""
        # Frame principal qui contient tout
        main_frame = tk.Frame(self.root, bg=self.COULEUR_FOND)
        main_frame.pack(side="top", fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # ===================
        # SIDEBAR (GAUCHE)
        # ===================
        self.sidebar_frame = tk.Frame(main_frame, bg=self.COULEUR_SIDEBAR, width=250)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.grid_propagate(False)
        
        # Titre de la sidebar
        title_label = tk.Label(
            self.sidebar_frame,
            text=" Bibliothèque",
            font=('Segoe UI', 18, 'bold'),
            bg=self.COULEUR_SIDEBAR,
            fg=self.COULEUR_TEXTE_CLAIR
        )
        title_label.pack(pady=25, padx=20)
        
        # Separator
        separator = tk.Frame(self.sidebar_frame, bg=self.COULEUR_PRIMAIRE, height=2)
        separator.pack(fill="x", padx=20, pady=10)
        
        # Menu buttons container
        menu_container = tk.Frame(self.sidebar_frame, bg=self.COULEUR_SIDEBAR)
        menu_container.pack(fill="both", expand=True, padx=15, pady=20)
        
        # Boutons de navigation
        self.dashboard_btn = self._create_menu_button(
            menu_container,
            " Dashboard",
            self.show_dashboard
        )
        self.dashboard_btn.pack(fill="x", pady=8)
        
        self.add_book_btn = self._create_menu_button(
            menu_container,
            " Ajouter un livre",
            self.show_add_book
        )
        self.add_book_btn.pack(fill="x", pady=8)
        
        self.view_books_btn = self._create_menu_button(
            menu_container,
            " Afficher les livres",
            self.show_books
        )
        self.view_books_btn.pack(fill="x", pady=8)
        
        self.stats_btn = self._create_menu_button(
            menu_container,
            " Statistiques",
            self.show_statistics
        )
        self.stats_btn.pack(fill="x", pady=8)
        
        # Footer dans la sidebar
        footer_label = tk.Label(
            self.sidebar_frame,
            text="© 2026\nMaria Ounassar\nOumayma Zahri\nAimane Rahmani",
            font=('Segoe UI', 7),
            bg=self.COULEUR_SIDEBAR,
            fg="#95A5A6",
            justify="center"
        )
        footer_label.pack(side="bottom", pady=15)
        
        # ===================
        # CONTENT AREA (DROITE)
        # ===================
        self.content_frame = tk.Frame(main_frame, bg=self.COULEUR_FOND)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_propagate(True)
    
    def _create_menu_button(self, parent, text, command):
        """
        Crée un bouton de menu de la sidebar.
        
        Args:
            parent: Widget parent
            text: Texte du bouton
            command: Fonction callback
            
        Returns:
            Bouton créé
        """
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Segoe UI', 11, 'bold'),
            bg=self.COULEUR_PRIMAIRE,
            fg=self.COULEUR_TEXTE_CLAIR,
            padx=15,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.COULEUR_BOUTON_HOVER,
            activeforeground=self.COULEUR_TEXTE_CLAIR
        )
        return btn
    
    def _clear_content(self):
        """Nettoie la zone de contenu (content_frame)."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # ===================
    # PAGES
    # ===================
    
    def show_dashboard(self):
        """Affiche la page Dashboard."""
        self._clear_content()
        self.current_page = "dashboard"
        
        # En-tête
        header_frame = tk.Frame(self.content_frame, bg=self.COULEUR_PRIMAIRE, height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        title = tk.Label(
            header_frame,
            text="Bienvenue dans votre Bibliothèque",
            font=('Segoe UI', 28, 'bold'),
            bg=self.COULEUR_PRIMAIRE,
            fg=self.COULEUR_TEXTE_CLAIR
        )
        title.pack(pady=20)
        
        # Contenu principal
        content = tk.Frame(self.content_frame, bg=self.COULEUR_FOND)
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Message de bienvenue
        welcome_label = tk.Label(
            content,
            text="Gestion de Bibliothèque",
            font=('Segoe UI', 20, 'bold'),
            bg=self.COULEUR_FOND,
            fg=self.COULEUR_TEXTE
        )
        welcome_label.pack(pady=20)
        
        desc_label = tk.Label(
            content,
            text="Système professionnel de gestion et d'organisation de vos livres.\n\n"
                 "Utilisez les boutons du menu pour:\n"
                 "• Ajouter de nouveaux livres à votre collection\n"
                 "• Consulter et rechercher vos livres\n"
                 "• Gérer les informations de chaque livre\n"
                 "• Consulter les statistiques de votre bibliothèque",
            font=('Segoe UI', 12),
            bg=self.COULEUR_FOND,
            fg=self.COULEUR_TEXTE,
            justify="left"
        )
        desc_label.pack(pady=20)
        
        # Stats rapides
        stats = self.db.get_statistics()
        stats_frame = tk.Frame(content, bg=self.COULEUR_FOND)
        stats_frame.pack(fill="x", pady=30)
        
        tk.Label(
            stats_frame,
            text=f" Total de livres: {stats['total_livres']}",
            font=('Segoe UI', 14, 'bold'),
            bg=self.COULEUR_FOND,
            fg=self.COULEUR_SECONDAIRE
        ).pack(pady=5)
        
        tk.Label(
            stats_frame,
            text=f" Quantité totale: {stats['quantité_totale']}",
            font=('Segoe UI', 14, 'bold'),
            bg=self.COULEUR_FOND,
            fg=self.COULEUR_SUCCES
        ).pack(pady=5)
        
        tk.Label(
            stats_frame,
            text=f" Catégories: {stats['catégories_uniques']}",
            font=('Segoe UI', 14, 'bold'),
            bg=self.COULEUR_FOND,
            fg=self.COULEUR_ACCENT
        ).pack(pady=5)
    
    def show_add_book(self):
        """Affiche la page Ajouter un livre."""
        self._clear_content()
        self.current_page = "add_book"
        
        # En-tête
        header_frame = tk.Frame(self.content_frame, bg=self.COULEUR_PRIMAIRE, height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        title = tk.Label(
            header_frame,
            text="Ajouter un nouveau livre",
            font=('Segoe UI', 24, 'bold'),
            bg=self.COULEUR_PRIMAIRE,
            fg=self.COULEUR_TEXTE_CLAIR
        )
        title.pack(pady=20)
        
        # Content area
        content = tk.Frame(self.content_frame, bg=self.COULEUR_FOND)
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Scrollable content
        canvas = tk.Canvas(content, bg=self.COULEUR_FOND, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Formulaire
        form_frame = tk.Frame(scrollable_frame, bg=self.COULEUR_FOND)
        form_frame.pack(fill="x", padx=10)
        
        # Titre
        tk.Label(form_frame, text="Titre:", font=('Segoe UI', 10, 'bold'), bg=self.COULEUR_FOND, fg=self.COULEUR_TEXTE).pack(anchor="w", pady=(10, 0))
        self.entry_titre = tk.Entry(form_frame, font=('Segoe UI', 10), width=50)
        self.entry_titre.pack(fill="x", pady=(0, 10))
        
        # Auteur
        tk.Label(form_frame, text="Auteur:", font=('Segoe UI', 10, 'bold'), bg=self.COULEUR_FOND, fg=self.COULEUR_TEXTE).pack(anchor="w", pady=(10, 0))
        self.entry_auteur = tk.Entry(form_frame, font=('Segoe UI', 10), width=50)
        self.entry_auteur.pack(fill="x", pady=(0, 10))
        
        # Année
        tk.Label(form_frame, text="Année:", font=('Segoe UI', 10, 'bold'), bg=self.COULEUR_FOND, fg=self.COULEUR_TEXTE).pack(anchor="w", pady=(10, 0))
        self.entry_annee = tk.Entry(form_frame, font=('Segoe UI', 10), width=50)
        self.entry_annee.pack(fill="x", pady=(0, 10))
        
        # Catégorie
        tk.Label(form_frame, text="Catégorie:", font=('Segoe UI', 10, 'bold'), bg=self.COULEUR_FOND, fg=self.COULEUR_TEXTE).pack(anchor="w", pady=(10, 0))
        self.entry_categorie = tk.Entry(form_frame, font=('Segoe UI', 10), width=50)
        self.entry_categorie.pack(fill="x", pady=(0, 10))
        
        # ISBN
        tk.Label(form_frame, text="ISBN:", font=('Segoe UI', 10, 'bold'), bg=self.COULEUR_FOND, fg=self.COULEUR_TEXTE).pack(anchor="w", pady=(10, 0))
        self.entry_isbn = tk.Entry(form_frame, font=('Segoe UI', 10), width=50)
        self.entry_isbn.pack(fill="x", pady=(0, 10))
        
        # Quantité
        tk.Label(form_frame, text="Quantité:", font=('Segoe UI', 10, 'bold'), bg=self.COULEUR_FOND, fg=self.COULEUR_TEXTE).pack(anchor="w", pady=(10, 0))
        self.entry_quantite = tk.Entry(form_frame, font=('Segoe UI', 10), width=50)
        self.entry_quantite.pack(fill="x", pady=(0, 10))
        
        # Image section
        tk.Label(form_frame, text="Image de couverture:", font=('Segoe UI', 10, 'bold'), bg=self.COULEUR_FOND, fg=self.COULEUR_TEXTE).pack(anchor="w", pady=(20, 0))
        
        img_btn_frame = tk.Frame(form_frame, bg=self.COULEUR_FOND)
        img_btn_frame.pack(fill="x", pady=(0, 10))
        
        btn_upload = tk.Button(
            img_btn_frame,
            text=" Télécharger image",
            font=('Segoe UI', 10, 'bold'),
            bg=self.COULEUR_SECONDAIRE,
            fg=self.COULEUR_TEXTE_CLAIR,
            padx=10,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._upload_image
        )
        btn_upload.pack(side="left", fill="x", expand=True)
        
        # Image preview
        self.image_preview = tk.Label(
            form_frame,
            text="Aucune image",
            font=('Segoe UI', 9),
            bg="#BDC3C7",
            fg=self.COULEUR_TEXTE_CLAIR,
            width=48,
            height=12
        )
        self.image_preview.pack(fill="both", expand=True, pady=(0, 20))
        
        # Save button
        btn_save = tk.Button(
            form_frame,
            text=" Ajouter/Modifier le livre",
            font=('Segoe UI', 11, 'bold'),
            bg=self.COULEUR_SUCCES,
            fg=self.COULEUR_TEXTE_CLAIR,
            padx=10,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._save_book
        )
        btn_save.pack(fill="x", pady=10)
        
        # Reset button
        btn_reset = tk.Button(
            form_frame,
            text=" Réinitialiser le formulaire",
            font=('Segoe UI', 11, 'bold'),
            bg="#95A5A6",
            fg=self.COULEUR_TEXTE_CLAIR,
            padx=10,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._clear_form
        )
        btn_reset.pack(fill="x", pady=(0, 10))
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_books(self):
        """Affiche la page Afficher les livres."""
        self._clear_content()
        self.current_page = "view_books"
        
        # En-tête
        header_frame = tk.Frame(self.content_frame, bg=self.COULEUR_PRIMAIRE, height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        title = tk.Label(
            header_frame,
            text="Gestion des livres",
            font=('Segoe UI', 24, 'bold'),
            bg=self.COULEUR_PRIMAIRE,
            fg=self.COULEUR_TEXTE_CLAIR
        )
        title.pack(pady=20)
        
        # Content area
        content = tk.Frame(self.content_frame, bg=self.COULEUR_FOND)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Barre de recherche
        search_frame = tk.Frame(content, bg=self.COULEUR_FOND)
        search_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            search_frame,
            text=" Rechercher:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.COULEUR_FOND,
            fg=self.COULEUR_TEXTE
        ).pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_change)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 10),
            width=40
        )
        search_entry.pack(side="left", fill="x", expand=True)
        
        # Tableau des livres
        table_frame = tk.Frame(content, bg=self.COULEUR_FOND)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        columns = ("ID", "Titre", "Auteur", "Année", "Catégorie", "Quantité")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=20,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configuration des colonnes
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("ID", anchor="center", width=40)
        self.tree.column("Titre", anchor="w", width=150)
        self.tree.column("Auteur", anchor="w", width=120)
        self.tree.column("Année", anchor="center", width=70)
        self.tree.column("Catégorie", anchor="w", width=100)
        self.tree.column("Quantité", anchor="center", width=80)
        
        # Headings
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Auteur", text="Auteur")
        self.tree.heading("Année", text="Année")
        self.tree.heading("Catégorie", text="Catégorie")
        self.tree.heading("Quantité", text="Quantité")
        
        # Bind
        self.tree.bind("<Double-1>", self._on_tree_double_click)
        
        self.tree.pack(fill="both", expand=True)
        
        # Boutons d'actions
        actions_frame = tk.Frame(content, bg=self.COULEUR_FOND)
        actions_frame.pack(fill="x", pady=(10, 0))
        
        btn_edit = tk.Button(
            actions_frame,
            text=" Éditer",
            font=('Segoe UI', 10, 'bold'),
            bg=self.COULEUR_SECONDAIRE,
            fg=self.COULEUR_TEXTE_CLAIR,
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._edit_selected
        )
        btn_edit.pack(side="left", padx=5)
        
        btn_delete = tk.Button(
            actions_frame,
            text=" Supprimer",
            font=('Segoe UI', 10, 'bold'),
            bg=self.COULEUR_ACCENT,
            fg=self.COULEUR_TEXTE_CLAIR,
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._delete_selected
        )
        btn_delete.pack(side="left", padx=5)
        
        # Rafraîchir le tableau
        self._update_tree()
    
    def show_statistics(self):
        """Affiche la page Statistiques."""
        self._clear_content()
        self.current_page = "statistics"
        
        # En-tête
        header_frame = tk.Frame(self.content_frame, bg=self.COULEUR_PRIMAIRE, height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        title = tk.Label(
            header_frame,
            text="Statistiques de la Bibliothèque",
            font=('Segoe UI', 24, 'bold'),
            bg=self.COULEUR_PRIMAIRE,
            fg=self.COULEUR_TEXTE_CLAIR
        )
        title.pack(pady=20)
        
        # Content
        content = tk.Frame(self.content_frame, bg=self.COULEUR_FOND)
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Récupérer les stats
        stats = self.db.get_statistics()
        
        # Créer les cartes
        self._create_stat_card(
            content,
            " Total de Livres",
            str(stats['total_livres']),
            self.COULEUR_SECONDAIRE,
            row=0,
            col=0
        )
        
        self._create_stat_card(
            content,
            " Quantité Totale",
            str(stats['quantité_totale']),
            self.COULEUR_ACCENT,
            row=0,
            col=1
        )
        
        self._create_stat_card(
            content,
            " Catégories Uniques",
            str(stats['catégories_uniques']),
            self.COULEUR_SUCCES,
            row=0,
            col=2
        )
        
        self._create_stat_card(
            content,
            " Auteur Fréquent",
            str(stats['auteur_frequent']),
            "#9B59B6",
            row=1,
            col=0,
            colspan=3
        )
    
    def _create_stat_card(self, parent, titre, valeur, couleur, row, col, colspan=1):
        """
        Crée une carte de statistique.
        
        Args:
            parent: Widget parent
            titre: Titre de la stat
            valeur: Valeur
            couleur: Couleur
            row: Ligne
            col: Colonne
            colspan: Nombre de colonnes
        """
        card = tk.Frame(
            parent,
            bg=couleur,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=2,
            highlightbackground=couleur
        )
        card.grid(row=row, column=col, columnspan=colspan, padx=20, pady=20, sticky="nsew")
        
        title_label = tk.Label(
            card,
            text=titre,
            font=('Segoe UI', 14, 'bold'),
            bg=couleur,
            fg=self.COULEUR_TEXTE_CLAIR
        )
        title_label.pack(pady=20)
        
        value_label = tk.Label(
            card,
            text=valeur,
            font=('Segoe UI', 32, 'bold'),
            bg=couleur,
            fg=self.COULEUR_TEXTE_CLAIR
        )
        value_label.pack(pady=20)
        
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
    
    # ===================
    # HELPERS
    # ===================
    
    def _upload_image(self):
        """Ouvre un dialogue pour télécharger une image."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif"), ("All", "*.*")]
        )
        
        if file_path:
            self.current_image_path = file_path
            try:
                img = Image.open(file_path)
                img.thumbnail((400, 300))
                photo = ImageTk.PhotoImage(img)
                self.image_preview.config(image=photo, text="")
                self.image_preview.image = photo
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger l'image: {e}")
    
    def _save_book(self):
        """Sauvegarde un livre (ajout ou modification)."""
        titre = self.entry_titre.get().strip()
        auteur = self.entry_auteur.get().strip()
        annee = self.entry_annee.get().strip()
        categorie = self.entry_categorie.get().strip()
        isbn = self.entry_isbn.get().strip()
        quantite = self.entry_quantite.get().strip()
        
        if not all([titre, auteur, annee, categorie, isbn, quantite]):
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires!")
            return
        
        try:
            annee = int(annee)
            quantite = int(quantite)
        except ValueError:
            messagebox.showerror("Erreur", "L'année et la quantité doivent être des nombres!")
            return
        
        if self.current_book_id is None:
            self.db.add_book(
                titre, auteur, annee, categorie, isbn, quantite,
                self.current_image_path or ""
            )
            messagebox.showinfo("Succès", "Livre ajouté avec succès!")
        else:
            self.db.update_book(
                self.current_book_id,
                titre=titre,
                auteur=auteur,
                année=annee,
                catégorie=categorie,
                isbn=isbn,
                quantité=quantite,
                chemin_image=self.current_image_path or ""
            )
            messagebox.showinfo("Succès", "Livre modifié avec succès!")
        
        self._clear_form()
        
        # Si on est sur la page afficher, rafraîchir
        if self.current_page == "add_book":
            self.show_add_book()
    
    def _clear_form(self):
        """Réinitialise le formulaire."""
        self.entry_titre.delete(0, tk.END)
        self.entry_auteur.delete(0, tk.END)
        self.entry_annee.delete(0, tk.END)
        self.entry_categorie.delete(0, tk.END)
        self.entry_isbn.delete(0, tk.END)
        self.entry_quantite.delete(0, tk.END)
        self.image_preview.config(image="", text="Aucune image")
        self.image_preview.image = None
        self.current_book_id = None
        self.current_image_path = None
    
    def _on_search_change(self, *args):
        """Callback pour les changements dans la barre de recherche."""
        if self.current_page == "view_books":
            query = self.search_var.get()
            self._update_tree(query)
    
    def _on_tree_double_click(self, event):
        """Double-clic sur une ligne du tableau."""
        if not hasattr(self, 'tree'):
            return
        
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, "values")
        
        if values:
            book_id = int(values[0])
            self._load_book_form(book_id)
    
    def _load_book_form(self, book_id):
        """Charge les données d'un livre dans le formulaire."""
        # Aller à la page add_book
        self.show_add_book()
        
        book = self.db.get_book_by_id(book_id)
        
        if book:
            self.entry_titre.delete(0, tk.END)
            self.entry_titre.insert(0, book["Title"])
            
            self.entry_auteur.delete(0, tk.END)
            self.entry_auteur.insert(0, book["Author"])
            
            self.entry_annee.delete(0, tk.END)
            self.entry_annee.insert(0, str(int(book["Year"])))
            
            self.entry_categorie.delete(0, tk.END)
            self.entry_categorie.insert(0, book["Category"])
            
            self.entry_isbn.delete(0, tk.END)
            self.entry_isbn.insert(0, book["ISBN"])
            
            self.entry_quantite.delete(0, tk.END)
            self.entry_quantite.insert(0, str(int(book["Quantity"])))
            
            self.current_book_id = book_id
            
            # Charger l'image si elle existe
            if book["ImagePath"] and os.path.exists(book["ImagePath"]):
                self.current_image_path = book["ImagePath"]
                try:
                    img = Image.open(book["ImagePath"])
                    img.thumbnail((400, 300))
                    photo = ImageTk.PhotoImage(img)
                    self.image_preview.config(image=photo, text="")
                    self.image_preview.image = photo
                except Exception as e:
                    print(f"Erreur de chargement d'image: {e}")
    
    def _edit_selected(self):
        """Édite le livre sélectionné."""
        if not hasattr(self, 'tree'):
            return
        
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre!")
            return
        
        item = selection[0]
        values = self.tree.item(item, "values")
        book_id = int(values[0])
        self._load_book_form(book_id)
    
    def _delete_selected(self):
        """Supprime le livre sélectionné."""
        if not hasattr(self, 'tree'):
            return
        
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre!")
            return
        
        item = selection[0]
        values = self.tree.item(item, "values")
        book_id = int(values[0])
        titre = values[1]
        
        if messagebox.askyesno("Confirmation", f"Supprimer '{titre}'?"):
            self.db.delete_book(book_id)
            messagebox.showinfo("Succès", "Livre supprimé!")
            if self.current_page == "view_books":
                self.show_books()
    
    def _update_tree(self, query=""):
        """Met à jour le tableau des livres."""
        if not hasattr(self, 'tree'):
            return
        
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Récupérer les livres
        if query:
            books_df = self.db.search_books(query)
        else:
            books_df = self.db.get_all_books()
        
        # Ajouter les livres au tableau
        for _, row in books_df.iterrows():
            self.tree.insert(
                "",
                "end",
                values=(
                    int(row["ID"]),
                    row["Title"],
                    row["Author"],
                    int(row["Year"]),
                    row["Category"],
                    int(row["Quantity"])
                )
            )
