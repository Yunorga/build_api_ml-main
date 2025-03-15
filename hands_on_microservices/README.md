# Description du projet MLOps TD

Le projet propose une interface basée sur deux API, une API pour les utilisateurs connectés et une API pour les utilisateurs non connectés, ces deux API permettent de communiquer avec une base de données, en offrant deux niveaux d’accès :

**Utilisateurs non authentifiés** :

Ces utilisateurs peuvent uniquement envoyer une image dessinée pour obtenir une prédiction de la forme qui y est représentée. Le backend traite l’image à l’aide d’un modèle de ML (actuellement simulé) et enregistre à la fois l’image et la prédiction dans la base de données. Ils peuvent également consulter la liste des images enregistrées avec leur tag associé, mais sans possibilité de modification.

**Utilisateurs authentifiés** :

Ces utilisateurs disposent d’un accès étendu qui leur permet de consulter les images enregistrées et, si nécessaire, de modifier le tag associé (par exemple, pour corriger une prédiction erronée). L’authentification est gérée via un token JWT, assurant ainsi une couche de sécurité pour la modification des données.

----

Ce projet présente une solution MLOps incluant :

- Un backend développé en FastAPI qui expose des endpoints pour prédire et stocker des images ainsi que pour mettre à jour les tags associés.

- Un frontend développé en Streamlit permettant aux utilisateurs de dessiner des formes, d'envoyer des images pour prédiction, de visualiser les images enregistrées et, pour les utilisateurs authentifiés, de mettre à jour les tags.
  
- Une base de données PostgreSQL qui stocke les images (sous forme binaire) et leur tag (forme prédite).

- L’orchestration de tous ces composants via Docker et docker-compose.


---

## Déroulé d'une séquence d'utilisation 

1) **Création et Soumission d’Image**

    L’utilisateur non authentifié dessine une forme sur un canvas (via Streamlit).
    En cliquant sur « Submit and Predict », l’image est encodée en base64 et envoyée au backend.

2) **Prédiction et Enregistrement**

    Le backend reçoit l’image, exécute le modèle de ML pour prédire la forme, puis stocke l’image et la prédiction dans la base de données PostgreSQL.
    La réponse (tag prédit) est renvoyée à l’utilisateur pour confirmation.

3) **Visualisation et Modification (Authentification requise)**

    L’interface affiche toutes les images enregistrées avec leur tag associé.
    L’utilisateur authentifié, après s’être connecté, peut modifier le tag de chaque image et soumettre une mise à jour via un endpoint sécurisé.

---

## Architecture

Le système est décomposé en trois parties principales, chacune fonctionnant dans son propre conteneur Docker :

- **Backend (FastAPI)** : Gère les appels API, l’authentification, la prédiction avec le modèle ML et la communication avec la base de données.

- **Frontend (Streamlit)** : Fournit une interface graphique permettant de dessiner, d’afficher les images et d’interagir avec l’API.

- **Base de données (PostgreSQL)** : Stocke les images et leurs informations associées.

---

## Instructions pour Builder et Démarrer le Projet

1. **Cloner le projet**  
    Ouvrez un terminal et clonez le repository :
    
    bash
    
    Copier le code
    
    `git clone <URL_DU_REPOSITORY> cd mlops_project`
    
2. **Builder les images Docker**  
    Dans le répertoire racine du projet, exécutez :
    
    bash
    
    Copier le code
    
    `docker-compose build`
    
3. **Démarrer les conteneurs**  
    Lancez l'ensemble des services avec :
    
    bash
    
    Copier le code
    
    `docker-compose up`
    
    Cette commande démarre :
    
    - Un conteneur **PostgreSQL** (port 5432)
    - Le conteneur **backend** (FastAPI sur le port 8000)
    - Le conteneur **frontend** (Streamlit sur le port 8501)

---

## Utilisation de l'Interface

1. **Accès à l'interface Streamlit**  
    Ouvrez votre navigateur à l'adresse suivante :  
    http://localhost:8501
    
2. **Navigation dans l’interface**  
    Dans la barre latérale, trois options sont disponibles :
    
    - **Non authentifié** :
        - Dessinez une forme sur le canvas.
        
        - Cliquez sur **"Submit and Predict"** pour envoyer l'image au backend. Le backend prédit la forme, enregistre l'image et affiche le résultat.

        - Vous pouvez également consulter la liste des images enregistrées ainsi que leur tag associé.

    - **Authentifié** :
        - Après vous être connecté via l'option **Login**, vous pouvez accéder à la visualisation des images et modifier le tag associé à chaque image.

    - **Login** :
        - Entrez vos identifiants pour obtenir un token d’authentification.

        - **Exemple de démo** :
            - Username : `admin`
            - Password : `admin`

---

# Réponse au questions du TD

## Partie 1

**Contexte Général**

**Nginx :**
Dans ce projet, Nginx n'est pas nécessaire car Docker Compose gère déjà le routage entre les conteneurs, et les serveurs intégrés de FastAPI et Streamlit suffisent pour une application de cette envergure. Nginx est généralement utilisé pour le load balancing, le caching ou la sécurisation en production, ce qui n'est pas le cas ici.

**Kubernetes (Minikube) :**
Migrer vers Kubernetes n'est pas indispensable car Docker Compose est simple et efficace pour le développement et le prototypage d'une application modeste comme celle-ci. Kubernetes offre une scalabilité avancée et une gestion fine des ressources, mais cela ajoute une complexité superflue pour ce projet de petite taille.


## Partie II – Un portail web adapté

Ce projet, comme décrit dans la section "Description du projet MLOps TD", correspond à une solution prenant en compte les éléments mentionnés dans la figure présente dans les consignes et répondant au cahier des charges illustré par la figure.

## Partie III – Un portail web pour tous les gouvernés (conception et architecture de système pour du ML)

Ce projet correspond à une plateforme d'annotation automatique