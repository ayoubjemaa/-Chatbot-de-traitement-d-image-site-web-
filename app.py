from flask import Flask, render_template, jsonify, Response, send_from_directory, request
import cv2
import os
import base64
import sympy as sp
from deepface import DeepFace
import numpy as np
import pytesseract
import tensorflow as tf
import re
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from PIL import Image
import threading

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialisation de la caméra et du modèle de détection
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Chargement du modèle MobileNetV2 pour la reconnaissance d'objets
mobilenet_model = tf.keras.applications.MobileNetV2(weights="imagenet")

def gen_frames():
    """Capture de flux vidéo avec détection de visages."""
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    """Route pour diffuser le flux vidéo."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/check_face')
def check_face():
    """Vérification de la détection d'un visage."""
    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Impossible de lire la vidéo"}), 400
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    message = "Visage détecté" if len(faces) > 0 else "Aucun visage détecté"
    return jsonify({"message": message})
@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyse l'âge et le sexe d'une personne à partir d'une image"""
    try:
        data = request.json  # Récupération des données JSON envoyées par la requête POST
        image1_data = data.get("image1")  # Extraction de l'image encodée en Base64
        
        if not image1_data:
            return jsonify({"error": "Aucune image reçue"}), 400  # Retourne une erreur si l'image est absente
        
        img_path = save_image(image1_data, "image1.jpg")  # Sauvegarde l'image et récupère son chemin
        
        # Analyse du visage avec DeepFace
        analysis = DeepFace.analyze(img_path, actions=['age', 'gender'], enforce_detection=False)
        
        # Récupération des résultats
        age = analysis[0].get('age', "Inconnu")  # Si la clé 'age' n'existe pas, retourne "Inconnu"
        gender = analysis[0].get('dominant_gender', "Inconnu")  # Même logique pour le genre

        return jsonify({"age": age, "gender": gender})  # Retourne les résultats en JSON

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Capture et renvoie toute erreur sous forme JSON


@app.route("/compare", methods=["POST"])
def compare_faces():
    """Comparaison de deux images ou reconnaissance d'un objet."""
    try:
        data = request.json
        image1_data = data.get("image1")
        image2_data = data.get("image2")
        
        if not image1_data:
            return jsonify({"error": "Au moins une image est requise."}), 400
        
        img1_path = save_image(image1_data, "image1.jpg")
        
        if image2_data:
            img2_path = save_image(image2_data, "image2.jpg")
            result = DeepFace.verify(img1_path, img2_path)
            return jsonify({"same_person": result["verified"], "distance": result["distance"]})
        
        object_name = recognize_object(img1_path)
        return jsonify({"object_name": object_name})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/recognize_text", methods=["POST"])
def recognize_text_route():
    """Reconnaissance de texte sur une image."""
    try:
        data = request.json
        image1_data = data.get("image1")
        if image1_data:
            img_path = save_image(image1_data, "image1.jpg")
            recognized_text = recognize_text(img_path)
            return jsonify({"recognized_text": recognized_text})
        return jsonify({"error": "Aucune image reçue."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/solve_equation", methods=["POST"])
def solve_equation():
    """Extraction et résolution d'une équation à partir d'une image."""
    try:
        data = request.json
        image_data = data.get("image1")

        if not image_data:
            return jsonify({"error": "Aucune image reçue."}), 400

        img_path = save_image(image_data, "image1.jpg")
        if not img_path:
            return jsonify({"error": "Erreur lors de l'enregistrement de l'image."}), 500

        # Extraction de l'équation de l'image
        extracted_equation = extract_equation(img_path)

        if not extracted_equation:
            return jsonify({"error": "Aucune équation détectée."}), 400

        # Résolution de l'équation extraite
        solutions = solve_expression(extracted_equation)

        return jsonify({
            "equation": extracted_equation,
            "solutions": solutions
        })

    except Exception as e:
        print(f"❌ Erreur dans solve_equation : {e}")  # DEBUG
        return jsonify({"error": str(e)}), 500

# Fonction pour extraire l'équation de l'image
def extract_equation(image_path):
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        equation_text = pytesseract.image_to_string(thresh, config="--psm 6")

        # Nettoyage du texte extrait
        equation_text = equation_text.replace("—", "-")
        equation_text = equation_text.replace("^", "**")
        equation_text = equation_text.replace(" ", "")

        # Correction : Ajouter un * manquant entre x et (
        equation_text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation_text)  # 3x → 3*x
        equation_text = re.sub(r'([a-zA-Z])\(', r'\1*(', equation_text)  # x(x-1) → x*(x-1)

          
        # Suppression des caractères indésirables à la fin de l'expression
        equation_text = re.sub(r'[^\d\w\s\+\-\*/\^\(\)=<>,.-]+$', '', equation_text)
        match = re.search(r'([0-9x\+\-\*/\^\(\)=<>]+)', equation_text)
        return match.group(0) if match else None
    except Exception as e:
        return f"Erreur : {e}"
# Fonction pour résoudre une équation ou une inéquation
def solve_expression(expression):
    try:
        print(expression)
        x = sp.Symbol('x')

        if "<=" in expression:
            left, right = expression.split("<=")
            solution = sp.solve_univariate_inequality(sp.sympify(left) <= sp.sympify(right), x)
        elif ">=" in expression:
            left, right = expression.split(">=")
            solution = sp.solve_univariate_inequality(sp.sympify(left) >= sp.sympify(right), x)
        elif "<" in expression:
            left, right = expression.split("<")
            solution = sp.solve_univariate_inequality(sp.sympify(left) < sp.sympify(right), x)
        elif ">" in expression:
            left, right = expression.split(">")
            solution = sp.solve_univariate_inequality(sp.sympify(left) > sp.sympify(right), x)
        elif "=" in expression:
            left, right = expression.split("=")
            equation = sp.sympify(left) - sp.sympify(right)
            solution = sp.solve(equation, x)
        else:
            return "Expression invalide"
        print(solution)
        # Conversion des solutions en valeurs normales
        solution_normalized = []
        for sol in solution:
            if isinstance(sol, sp.Basic):
                solution_normalized.append(float(sol.evalf()))  # Convertit en float
            else:
                solution_normalized.append(sol)  # Si c'est déjà un nombre normal

        print(solution_normalized)
        return solution_normalized
    except Exception as e:
        return f"Erreur de résolution : {e}"

def save_image(base64_string, filename):
    """Sauvegarde une image à partir d'une chaîne base64."""
    try:
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        print(image_path)
        with open(image_path, "wb") as img_file:
            img_file.write(base64.b64decode(base64_string))
        return image_path
    except Exception as e:
        raise ValueError(f"Erreur de décodage de l'image : {e}")

def recognize_object(image_path):
    """Reconnaissance d'objets avec MobileNetV2."""
    try:
        img = Image.open(image_path).resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        preds = mobilenet_model.predict(img_array)
        decoded_predictions = decode_predictions(preds, top=1)[0][0][1]
        return decoded_predictions
    except Exception as e:
        return f"Erreur dans la reconnaissance de l'objet : {e}"

def recognize_text(image_path):
    """Reconnaissance de texte avec pytesseract."""
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        return f"Erreur dans la reconnaissance de texte : {e}"

@app.route('/stop_camera')
def stop_camera():
    """Libération de la caméra."""
    cap.release()
    return jsonify({"message": "Caméra libérée"})

@app.route('/')
def index():
    """Page d'accueil - amélioration pour charger plus rapidement"""
    # Démarrer la caméra en arrière-plan
    threading.Thread(target=init_camera).start()
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

def init_camera():
    """Initialisation de la caméra pour un démarrage plus rapide"""
    cap.read()

@app.route("/chatbot.html")
def chatbot():
    """Page du chatbot."""
    return send_from_directory(os.path.join(app.root_path, 'static'), 'chatbot.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
