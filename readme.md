
Voici une structure complète pour démarrer avec Docker dès le début pour votre projet FastAPI. Nous allons inclure les fichiers nécessaires et les étapes pour configurer et exécuter votre environnement.

1. Arborescence du projet

DevIA/
├── app_api/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
├── data_api/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
├── docker-compose.yml
├── .env

Construire les conteneurs dans le répertoire racine de votre projet (C:\Users\Utilisateur\Documents\DevIA), en exécutant la commande bash suivante pour construire les images Docker des deux APIs : docker-compose build
Docker construit les images en suivant les Dockerfile définis dans chaque sous-dossier (app_api et data_api).
![alt text](image-1.png)
PS C:\Users\Utilisateur\Documents\DevIA> docker images
REPOSITORY       TAG       IMAGE ID       CREATED              SIZE
devia-app_api    latest    bb545ce1c3c6   About a minute ago   224MB
devia-data_api   latest    3af9019e3b53   About a minute ago   221MB

Lancer les services
Démarrer les conteneurs avec la commande bash : docker-compose up
Vérifier les logs de démarrage des deux APIs : uvicorn démarre correctement et les ports 8000 (pour app_api) et 9000 (pour data_api) sont exposés.
![alt text](image-2.png)

Tester les services
![alt text](image-3.png)
Interaction entre les APIs
![alt text](image-5.png)

Résultat: les tests ont été exécutés avec succès.
1. data_api/tests/test_data.py :
    - Le test a été détecté et exécuté correctement.
    - Indique que les fonctionnalités de data_api fonctionnent comme prévu.
2. app_api/tests/test_app.py :
    - Deux tests ont été détectés et ont réussi.
    - Cela montre que l'API principale et ses interactions simulées avec data_api sont en bon état.

suite
Prochaine étape possible
Ajout de tests supplémentaires :

Ajoutez des tests pour d'autres endpoints ou cas spécifiques.
Testez les cas d'erreurs ou de gestion d'exceptions.
Automatisation avec CI/CD :

Intégrez vos tests dans une pipeline CI/CD pour exécuter automatiquement les tests à chaque mise à jour du code.
Rapports de couverture :

Utilisez pytest-cov pour mesurer la couverture des tests :
bash
Copier le code
pip install pytest-cov
pytest --cov=app_api --cov=data_api
