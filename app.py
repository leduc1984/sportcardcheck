from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import json
from ebaysdk.finding import Connection as Finding
import cv2
import re
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration Flask
app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CACHE_FILE = 'cache.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Charger les informations d'authentification eBay depuis les variables d'environnement
EBAY_APP_ID = os.getenv('EBAY_APP_ID')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Prétraitement de l'image avec OpenCV
def preprocess_image(image_path):
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Erreur : impossible de lire l'image à partir de {image_path}")
            return None
        _, processed_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processed_image = cv2.GaussianBlur(processed_image, (5, 5), 0)
        processed_image_path = "preprocessed_" + os.path.basename(image_path)
        cv2.imwrite(processed_image_path, processed_image)
        return processed_image_path
    except Exception as e:
        print(f"Erreur lors du prétraitement de l'image : {e}")
        return None

# Extraction du texte avec OCR
def extract_text_from_image(image_path):
    processed_image_path = preprocess_image(image_path)
    if not processed_image_path:
        return "Erreur lors du prétraitement de l'image."
    try:
        text = pytesseract.image_to_string(processed_image_path)
        return text if text.strip() else "Aucun texte extrait."
    except Exception as e:
        print(f"Erreur lors de l'OCR : {e}")
        return "Erreur lors de l'OCR."

# Nettoyage du texte extrait
def clean_text(text):
    # Garder les mots alphanumériques et les caractères spéciaux pertinents
    cleaned_text = re.sub(r'[^A-Za-z0-9\s&]', '', text)
    return cleaned_text.strip()

# Recherche eBay avec différentes variantes de requêtes
def search_ebay(query):
    api = Finding(appid=EBAY_APP_ID, config_file=None)
    search_variants = [
        query,  # Requête originale
        ' '.join(query.split()[:2]),  # Les deux premiers mots seulement
        ' '.join(query.split()[:3]),  # Les trois premiers mots
        ' '.join(query.split()[-2:])  # Les deux derniers mots
    ]

    for variant in search_variants:
        try:
            response = api.execute('findItemsByKeywords', {'keywords': variant})
            if response.reply.ack != 'Success':
                print(f"La requête n'a pas été réussie pour : {variant}")
                continue

            items = getattr(response.reply.searchResult, 'item', None)
            if items:
                print(f"Des résultats ont été trouvés pour la requête : {variant}")
                return [{'title': item.title, 'price': item.sellingStatus.currentPrice.value, 'url': item.viewItemURL} for item in items]

        except Exception as e:
            print(f"Erreur lors de la recherche eBay avec la requête '{variant}' : {e}")

    print("Aucun résultat trouvé sur eBay avec les variantes de recherche.")
    return []

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_cached_results(query):
    return load_cache().get(query)

def cache_results(query, results):
    cache = load_cache()
    cache[query] = results
    save_cache(cache)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier trouvé'}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Type de fichier non autorisé'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    extracted_text = extract_text_from_image(filepath)
    cleaned_text = clean_text(extracted_text)
    
    if "Erreur" in extracted_text:
        return jsonify({'error': extracted_text}), 500

    return jsonify({'message': 'Image reçue', 'extracted_text': cleaned_text}), 200

@app.route('/search_ebay', methods=['POST'])
def search_ebay_route():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Requête non spécifiée'}), 400

    cleaned_query = clean_text(query)
    cached_results = get_cached_results(cleaned_query)
    if cached_results:
        return jsonify({'results': cached_results}), 200

    ebay_results = search_ebay(cleaned_query)
    if not ebay_results:
        return jsonify({'error': 'Aucun résultat trouvé sur eBay.'}), 404

    cache_results(cleaned_query, ebay_results)
    return jsonify({'results': ebay_results}), 200

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

