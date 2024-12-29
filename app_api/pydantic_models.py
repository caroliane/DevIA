""" Ce script définit la structure de nos données de requête et de réponse attendues en utilisant Pydantic, 
bibliothèque de validation de données qui utilise des annotations de type Python pour définir des schémas de données.
Indispensable pour le point de terminaison de la discussion.
"""

from pydantic import BaseModel, HttpUrl, field_validator  # pour la validation et la définition des modèles de données
from enum import Enum  # pour définir des choix fixes (ex. types de modèles)
from datetime import datetime  # Gestion des dates et heures

# Modèle de données pour les informations sur une URL YouTube chargée
class YoutubeUrlInfo(BaseModel):
    url: HttpUrl  # URL YouTube à télécharger
    upload_timestamp: datetime  # Date et heure du téléchargement

    @classmethod
    def validate_url(cls, url: str):
        if not url.startswith("https://www.youtube.com/watch"):
            raise ValueError("L'URL doit être une URL YouTube valide.")
        return url
    
    # @field_validator("url")
    # def validate_youtube_url(cls, value):
    #     url_str = str(value)  # Convertir HttpUrl en chaîne
    #     if "youtube.com" not in url_str and "youtu.be" not in url_str:
    #         raise ValueError("L'URL doit être une URL YouTube valide.")
    #     return value