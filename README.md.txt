# eBay Sports Card Recognition

This project is an application for recognizing sports cards using images. The app allows users to upload an image or use their webcam to take a picture of a sports card. The system then performs Optical Character Recognition (OCR) to extract relevant text and searches for the card on eBay. The goal is to find listings on eBay that match the recognized card.

## Features

- Upload an image or use the webcam to capture a photo of the sports card.
- Automatic OCR processing to extract text from the card.
- eBay search integration to find matching cards.
- Automatic backups using Git.
- Results displayed in a console-like style and formatted to look similar to eBay listings.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/leduc1984/sportcardcheck.git
Install the required dependencies:

Make sure you have Python and pip installed. Then, run:

bash
Copier le code
pip install -r requirements.txt
Set up your environment variables:

Create a .env file at the root of the project and add your eBay API credentials:

makefile
Copier le code
EBAY_APP_ID=your-ebay-app-id
EBAY_CERT_ID=your-ebay-cert-id
EBAY_DEV_ID=your-ebay-dev-id
EBAY_TOKEN=your-ebay-token
Important: Do not include your .env file in the repository to protect your credentials. The .env file is used to configure your eBay API access.

Run the application:

bash
Copier le code
python app.py
Open your browser and navigate to http://127.0.0.1:5000 to use the application.

How to Use
Click on "Activate Webcam" to use your camera or "Upload an Image" to choose an image file.
Once the image is uploaded, click "Go" to start the OCR and eBay search process.
The console will display progress, and the results will appear below, formatted similarly to eBay listings.
Program Description
The eBay Sports Card Recognition application is a tool designed to help collectors and sellers of sports cards quickly identify cards by using image recognition and OCR technology. The program scans an uploaded image or a photo taken with the webcam, extracts the text using OCR, and searches for matching items on eBay. The aim is to facilitate finding cards on the market that match the user's collection.

Contributing
If you would like to contribute to the growth of this project, here’s how you can help:

Feature Suggestions: Propose new features or enhancements.
Bug Reporting: Report any bugs or issues you encounter.
Code Contributions: Submit pull requests for improvements or bug fixes.
Documentation: Help improve or translate the documentation.
Feel free to open issues and make pull requests. Contributions are highly appreciated!

License
This project is licensed under the MIT License.

Version Française
Reconnaissance de Cartes de Sport sur eBay
Ce projet est une application pour la reconnaissance de cartes de sport à partir d'images. L'application permet aux utilisateurs de télécharger une image ou d'utiliser leur webcam pour prendre une photo d'une carte de sport. Le système effectue ensuite une reconnaissance optique de caractères (OCR) pour extraire le texte pertinent et recherche la carte sur eBay. L'objectif est de trouver des annonces sur eBay correspondant à la carte reconnue.

Fonctionnalités
Télécharger une image ou utiliser la webcam pour capturer une photo de la carte de sport.
Traitement OCR automatique pour extraire le texte de la carte.
Intégration de la recherche eBay pour trouver les cartes correspondantes.
Sauvegardes automatiques avec Git.
Résultats affichés dans un style de console et formatés pour ressembler aux annonces eBay.
Installation
Cloner le dépôt :

bash
Copier le code
git clone https://github.com/leduc1984/sportcardcheck.git
Installer les dépendances requises :

Assurez-vous d'avoir Python et pip installés. Ensuite, exécutez :

bash
Copier le code
pip install -r requirements.txt
Configurer vos variables d'environnement :

Créez un fichier .env à la racine du projet et ajoutez vos identifiants API eBay :

makefile
Copier le code
EBAY_APP_ID=votre-ebay-app-id
EBAY_CERT_ID=votre-ebay-cert-id
EBAY_DEV_ID=votre-ebay-dev-id
EBAY_TOKEN=votre-ebay-token
Important : N'incluez pas votre fichier .env dans le dépôt pour protéger vos informations sensibles. Le fichier .env est utilisé pour configurer l'accès à l'API eBay.

Exécuter l'application :

bash
Copier le code
python app.py
Ouvrez votre navigateur et allez à http://127.0.0.1:5000 pour utiliser l'application.

Description du Programme
L'application de reconnaissance de cartes de sport sur eBay est un outil conçu pour aider les collectionneurs et les vendeurs de cartes de sport à identifier rapidement les cartes à l'aide de la reconnaissance d'images et de la technologie OCR. Le programme scanne une image téléchargée ou une photo prise avec la webcam, extrait le texte à l'aide de l'OCR, et recherche les éléments correspondants sur eBay. Le but est de faciliter la recherche de cartes sur le marché qui correspondent à la collection de l'utilisateur.

Contribuer
Si vous souhaitez contribuer à la croissance de ce projet, voici comment vous pouvez aider :

Suggestions de fonctionnalités : Proposez de nouvelles fonctionnalités ou des améliorations.
Signalement de bugs : Signalez les bugs ou les problèmes que vous rencontrez.
Contributions au code : Soumettez des pull requests pour des améliorations ou des corrections de bugs.
Documentation : Aidez à améliorer ou à traduire la documentation.
N'hésitez pas à ouvrir des issues et à faire des pull requests. Les contributions sont très appréciées !

Licence
Ce projet est sous licence MIT.