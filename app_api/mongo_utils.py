""" Ce script permet d'interagir avec MongoDB et gérer les collections dans la base "DevIA" :
- "application_logs" : gère les interactions utilisateur avec un système d'IA
- "yt_url_store" : stocke les urls youtube valides et les informations associées (timestamp de téléchargement)
- "yt_data" : stocke la transcription et les métadonnées récupérées avec langchain_community.document_loaders Youtubeloader pour chaque nouvelle url youtube validée).
"""
import os
from pymongo import MongoClient
import mongomock  # Simulateur MongoDB pour les tests
from pymongo.errors import DuplicateKeyError
from datetime import datetime

DB_NAME = "Dev_IA"
COLLECTION_NAME_1 = "application_logs"
COLLECTION_NAME_2 = "yt_url_store"
COLLECTION_NAME_3 = "yt_data"

# Fonction pour obtenir la connexion MongoDB
def get_db_connection():
    """
    Renvoie une connexion à la base de données MongoDB.
    Utilise une base de données simulée (mongomock) si la variable d'environnement TESTING est définie.
    """
    if os.getenv("TESTING"):  # Si la variable d'environnement TESTING est définie
        client = mongomock.MongoClient()
    else:
        client = MongoClient("mongodb://mongodb:27017/")  # URI MongoDB pour production
    db = client[DB_NAME]  # MongoDB crée automatiquement la base si elle n'existe pas
    return db


# Fonction pour initialiser les collections (MongoDB crée automatiquement les collections si elles n'existent pas)
def create_application_logs():
    db = get_db_connection()
    """Crée un index sur `session_id` pour accélérer les requêtes basées sur cet identifiant"""
    db[COLLECTION_NAME_1].create_index("session_id")

def create_yt_url_store():
    db = get_db_connection()
    """Crée un index sur `url` pour éviter les doublons et améliorer les performances"""
    db[COLLECTION_NAME_2].create_index("url", unique=True)

def create_yt_data():
    db = get_db_connection()
    """Crée un index sur `source` pour éviter les doublons et améliorer les performances"""
    db[COLLECTION_NAME_3].create_index("source", unique=True)


def create_yt_url_store_index():
    """
    Crée un index unique sur le champ 'url' de la collection 'yt_url_store' pour éviter les doublons.
    """
    db = get_db_connection()
    db[COLLECTION_NAME_2].create_index("url", unique=True)
    print("Index unique créé sur le champ 'url' de la collection 'yt_url_store'.")

# Fonction pour insérer une nouvelle URL YouTube et son timestamp de téléchargement
def insert_yt_url_record(url):
    """
    Insère une nouvelle URL YouTube avec un horodatage.
    Gère les doublons et retourne un message d'erreur approprié.
    """
    db = get_db_connection()
    yt_url_entry = {
        "url": str(url),  # Convertir HttpUrl en chaîne
        "upload_timestamp": datetime.utcnow()
    }
    try:
        result = db[COLLECTION_NAME_2].insert_one(yt_url_entry)
        return {"message": "L'URL YouTube a été ajoutée avec succèss.", "id": str(result.inserted_id)}
    except DuplicateKeyError as e:
        raise DuplicateKeyError("L'URL YouTube est déjà enregistrée.") from e
    # except DuplicateKeyError:
    #     return {"message": "L'URL YouTube est déjà enregistrée."}
