# -Chatbot-de-traitement-d-image-site-web-
## 📌 Description Générale
Ce projet est un chatbot web intelligent capable d'analyser et de traiter des images et du texte via des requêtes utilisateur. Il combine des techniques avancées de vision par ordinateur (CV), de traitement automatique du langage (NLP) et de machine learning pour fournir des réponses interactives et précises.développé avec Python (Flask) côté serveur et HTML/CSS/JS côté client.
---
## 🚀 Fonctionnalités Principales

1/🧑‍🤝‍🧑 Analyse Faciale (DeepFace + OpenCV)

Comparaison de visages avec calcul de distance de similarité
Détection d'âge et sexe avec estimation de confiance
Intervalles de similarité:
Distance < 0.30: Très forte similarité (probablement la même personne)
0.30 ≤ Distance < 0.50: Similarité moyenne (possiblement la même personne)
Distance ≥ 0.50: Faible similarité (personnes différentes)

cas de succés ✅  : 

![image](https://github.com/user-attachments/assets/4093a30c-a267-47c8-b4ce-f62cb480373c)
![image](https://github.com/user-attachments/assets/7194d5d5-8322-4339-8594-7a2ec4ba6bcd)

cas d'échec ❌ :

![image](https://github.com/user-attachments/assets/77214f67-b97b-45d2-aef6-95092a1d1866)
![image](https://github.com/user-attachments/assets/a06908d3-1dd4-406c-b2b5-e3eb633f9366)

2/🔤 Reconnaissance de Texte (PyOCR)

Extraction de texte depuis les images
Support multilingue
Traitement post-OCR pour améliorer la précision

![image](https://github.com/user-attachments/assets/7b0b3731-8f43-4fca-8164-8928e9121db1)

3/➗ Résolution d'Équations Mathématiques (PyOCR + SymPy)

![image](https://github.com/user-attachments/assets/ba7b8ba2-7f7e-4a84-a7e0-0684e53505a4)

4/🧮 Détection d'Objets (MobileNetV2 + TensorFlow)

Reconnaissance de 1000 classes d'objets
Score de confiance pour chaque détection
Visualisation des bounding boxes

![image](https://github.com/user-attachments/assets/a784e238-54b9-45bb-a492-60cb8fb1e0e7)

5/détection de l'age et du sexe d'une personne (Deepface):

![image](https://github.com/user-attachments/assets/2bb6e577-5462-43fc-b8a3-26d2f6294af4)

---

## ⚙️ Technologies utilisées

🖥️ Backend Principal
Python 3.8+ (Langage principal)
Flask (Framework web léger)

🧠 Traitement d'Images et Vision par Ordinateur

OpenCV (cv2) - Lecture/écriture d'images et prétraitement
DeepFace - Analyse faciale avancée
Facenet, VGG-Face, OpenFace (modèles embarqués)
Détection de similarité (Distance L2)
Estimation d'âge et de genre
Dlib - Détection des points caractéristiques du visage
TensorFlow 2.x - Infrastructure de deep learning
Keras - API haut niveau pour les modèles

🔤 Reconnaissance de Texte (OCR)

PyOCR (Wrapper pour moteurs OCR)
Tesseract OCR (Moteur principal)

➗ Traitement Mathématique

SymPy - Résolution symbolique d'équations
NumPy - Calculs numériques
SciPy - Fonctions mathématiques avancées

🧮 Détection d'Objets
TensorFlow Object Detection API
MobileNetV2 (Modèle léger pré-entraîné)

🌐 Frontend Web

HTML5 - Structure de base
CSS3 (Flexbox/Grid) - Mise en page responsive
JavaScript ES6+ - Interactivité
Bootstrap 5 - Framework CSS

📦 Gestion des Dépendances
pip - Gestion des packages Python

🛠️ Outils de Développement

Git - Contrôle de version
VsCode - Prototypage des algorithmes

🤖Modèles Pré-entraînés

shape_predictor_68_face_landmarks.dat (Dlib)
mobilenet_v2_1.0_224 (TensorFlow Hub)
Age/Gender Model (DeepFace)
---
## 📁Structure du Projet
```
chatbot-traitement-image/
├── static/              # Fichiers statiques (CSS, JS, images)
├── uploads/             # Dossier pour les images uploadées
├── app.py               # Application principale (Flask)
├── README.md            # Ce fichier
└── shape_predictor_68_face_landmarks.dat  # Modèle pour la détection faciale
```
## Structure Technique

![deepseek_mermaid_20250504_b9481c](https://github.com/user-attachments/assets/aee3a8c9-9c37-4551-b693-4e3bd8c23205)

---
## ⚙️Installation

1/Prérequis

```
pip install deepface opencv-python pyocr tensorflow sympy
```

2/Télécharger les modèles:

```
wget http://example.com/shape_predictor_68_face_landmarks.dat
wget http://example.com/mobilenet_v2_weights.h5
````

3/Clonez le dépôt:

```
git clone https://github.com/ayoubjemaa/chatbot-traitement-image.git
cd chatbot-traitement-image
```

4/Installez les dépendances:

```
pip install -r requirements.txt  # Si disponible
```

5/Lancez l'application:

```
python app.py
```

6/Accédez à l'interface:

```
http://localhost:5000
```

