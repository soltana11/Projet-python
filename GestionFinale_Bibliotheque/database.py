
import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Optional

class LibraryDatabase:
    """
    Classe pour gérer toutes les opérations de base de données.
    Stocke les données dans un fichier CSV avec Pandas DataFrame.
    """
    
    def __init__(self, csv_path: str = "data/library.csv"):
        
        self.csv_path = csv_path
        self.df = self._load_or_create_database()
    
    def _load_or_create_database(self) -> pd.DataFrame:
       
       
        # Créer le répertoire data s'il n'existe pas
        Path(self.csv_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Colonnes de la base de données
        columns = ["ID", "Title", "Author", "Year", "Category", "ISBN", "Quantity", "ImagePath"]
        
        # Charger ou créer le fichier CSV
        if os.path.exists(self.csv_path):
            try:
                df = pd.read_csv(self.csv_path)
                return df
            except Exception as e:
                print(f"Erreur lors de la lecture du CSV: {e}")
                return pd.DataFrame(columns=columns)
        else:
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.csv_path, index=False)
            return df
    
    def save_to_csv(self) -> None:
        """Sauvegarde le DataFrame dans le fichier CSV."""
        try:
            self.df.to_csv(self.csv_path, index=False, encoding='utf-8')
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            raise
    
    def add_book(self, titre: str, auteur: str, année: int, 
                 catégorie: str, isbn: str, quantité: int, 
                 chemin_image: str = "") -> int:
       
        # Générer un ID unique
        new_id = int(self.df["ID"].max()) + 1 if len(self.df) > 0 else 1
        
        # Créer une nouvelle ligne
        new_row = {
            "ID": new_id,
            "Title": titre,
            "Author": auteur,
            "Year": int(année),
            "Category": catégorie,
            "ISBN": isbn,
            "Quantity": int(quantité),
            "ImagePath": chemin_image
        }
        
        # Ajouter la ligne au DataFrame
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Sauvegarder
        self.save_to_csv()
        
        return new_id
    
    def get_all_books(self) -> pd.DataFrame:
        """
        Retourne tous les livres de la base de données.
        
        Returns:
            DataFrame avec tous les livres
        """
        return self.df.copy()
    
    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        """
        Récupère un livre par son ID.
        
        Args:
            book_id: ID du livre
            
        Returns:
            Dictionnaire avec les données du livre ou None
        """
        book = self.df[self.df["ID"] == book_id]
        if not book.empty:
            return book.iloc[0].to_dict()
        return None
    
    def search_books(self, query: str) -> pd.DataFrame:
        """
        Recherche des livres par titre, auteur, catégorie ou ISBN.
        
        Args:
            query: Texte de recherche
            
        Returns:
            DataFrame avec les livres correspondants
        """
        query = query.lower()
        mask = (
            self.df["Title"].str.lower().str.contains(query, na=False) |
            self.df["Author"].str.lower().str.contains(query, na=False) |
            self.df["Category"].str.lower().str.contains(query, na=False) |
            self.df["ISBN"].str.lower().str.contains(query, na=False)
        )
        return self.df[mask].copy()
    
    def update_book(self, book_id: int, titre: str = None, auteur: str = None,
                    année: int = None, catégorie: str = None, isbn: str = None,
                    quantité: int = None, chemin_image: str = None) -> bool:
        """
        Met à jour les informations d'un livre.
        
        Args:
            book_id: ID du livre à mettre à jour
            titre: Nouveau titre (optionnel)
            auteur: Nouvel auteur (optionnel)
            année: Nouvelle année (optionnel)
            catégorie: Nouvelle catégorie (optionnel)
            isbn: Nouveau ISBN (optionnel)
            quantité: Nouvelle quantité (optionnel)
            chemin_image: Nouveau chemin image (optionnel)
            
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        idx = self.df[self.df["ID"] == book_id].index
        
        if len(idx) == 0:
            return False
        
        idx = idx[0]
        
        # Mettre à jour les champs fournis
        if titre is not None:
            self.df.at[idx, "Title"] = titre
        if auteur is not None:
            self.df.at[idx, "Author"] = auteur
        if année is not None:
            self.df.at[idx, "Year"] = int(année)
        if catégorie is not None:
            self.df.at[idx, "Category"] = catégorie
        if isbn is not None:
            self.df.at[idx, "ISBN"] = isbn
        if quantité is not None:
            self.df.at[idx, "Quantity"] = int(quantité)
        if chemin_image is not None:
            self.df.at[idx, "ImagePath"] = chemin_image
        
        self.save_to_csv()
        return True
    
    def delete_book(self, book_id: int) -> bool:
        """
        Supprime un livre de la base de données.
        
        Args:
            book_id: ID du livre à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        initial_len = len(self.df)
        self.df = self.df[self.df["ID"] != book_id]
        
        if len(self.df) < initial_len:
            self.save_to_csv()
            return True
        return False
    
    def get_statistics(self) -> Dict:
        """
        Calcule les statistiques de la bibliothèque.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        if len(self.df) == 0:
            return {
                "total_livres": 0,
                "quantité_totale": 0,
                "catégories_uniques": 0,
                "auteur_frequent": "N/A"
            }
        
        stats = {
            "total_livres": len(self.df),
            "quantité_totale": int(self.df["Quantity"].sum()),
            "catégories_uniques": int(self.df["Category"].nunique()),
            "auteur_frequent": self.df["Author"].mode()[0] if len(self.df["Author"].mode()) > 0 else "N/A"
        }
        return stats
    
    def get_categories(self) -> List[str]:
        """
        Retourne la liste des catégories uniques.
        
        Returns:
            Liste des catégories
        """
        return sorted(self.df["Category"].unique().tolist())
    
    def get_category_distribution(self) -> Dict[str, int]:
        """
        Retourne la distribution des livres par catégorie.
        
        Returns:
            Dictionnaire avec le nombre de livres par catégorie
        """
        return self.df["Category"].value_counts().to_dict()
