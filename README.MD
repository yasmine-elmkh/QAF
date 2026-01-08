# QAF - Chatbot Web Application

## 1. Description du projet
QAF est une application web basée sur une architecture en **trois couches** :
- **Front-end** : interface utilisateur interactive (HTML, CSS, JS).
- **Back-end** : API FastAPI pour gérer les requêtes du chatbot.
- **Base de données** : MySQL pour stocker les FAQ et réponses du chatbot.

L’objectif principal est de mettre en place une **pipeline DevOps automatisée** permettant la construction, le test et le déploiement automatique de l’application sur un **cluster Kubernetes** à chaque modification du code source.

---



## 2. Fonctionnalités principales
Chatbot intelligent basé sur IA/NLP, capable de comprendre le sens des questions et de répondre aux FAQ.
Utilisation de NLTK pour le prétraitement du texte : tokenisation, stopwords, lemmatisation.
Utilisation de Sentence-BERT pour encoder les questions et mesurer la similarité entre la question de l’utilisateur et celles stockées dans la base.
Interface utilisateur interactive et responsive.
Déploiement multi-conteneurs sur Kubernetes avec accès via Ingress.
CI/CD automatisée pour construire, tester et déployer automatiquement chaque modification du code.
---

## 3. Architecture


User
└─ Frontend (React/HTML+JS+CSS)
└─ Ingress → Routes → Backend (FastAPI)
└─ Database (MySQL)


- **Frontend** : déployé dans un container Nginx.
- **Backend** : déployé dans un container Python avec FastAPI.
- **MySQL** : container officiel MySQL pour la persistance des données.
- **Ingress** : gère les chemins `/api/*` vers le backend et `/` vers le frontend.
- **Services Kubernetes** : `ClusterIP` pour backend, `LoadBalancer` pour frontend.

---

## 4. Docker
Chaque couche est conteneurisée :
- **Backend Dockerfile** : installe Python, dépendances, NLTK, et lance FastAPI sur le port 8000.
- **Frontend Dockerfile** : utilise Nginx pour servir les fichiers statiques sur le port 80.
- **MySQL** : conteneur officiel avec secrets pour les credentials.

```bash
# Construire les images
docker build -t qaf-backend ./backend
docker build -t qaf-frontend ./frontend

5. Déploiement Kubernetes

Fichiers inclus dans k8s/ :

backend-deployment.yaml : deployment backend + probes + secrets

frontend-deployment.yaml : deployment frontend

backend-service.yaml : ClusterIP service backend

frontend-service.yaml : LoadBalancer service frontend

ingress.yaml : routage des chemins /api/* et / via Ingress

# Déployer sur Kubernetes
kubectl apply -f k8s/
kubectl get pods,svc,ingress


Accéder via navigateur :

Frontend : http://qaf.local/

