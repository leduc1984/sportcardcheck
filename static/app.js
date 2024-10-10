// Sélection des éléments HTML
const video = document.getElementById('camera');
const startWebcamBtn = document.getElementById('start-webcam-btn');
const uploadBtn = document.getElementById('upload-btn');
const goBtn = document.getElementById('go-btn');
const canvas = document.getElementById('canvas');
const previewImage = document.getElementById('captured-image');
const uploadInput = document.createElement('input');
uploadInput.type = 'file';
uploadInput.accept = 'image/*';
const resultsContainer = document.getElementById('results');
const progressBar = document.getElementById('progress-bar');
const consoleLog = document.getElementById('console-log');
const cameraContainer = document.getElementById('camera-container');

// Fonction pour simuler un effet de frappe
function typeConsoleMessage(message, delay = 50) {
    const messageElement = document.createElement('div');
    consoleLog.appendChild(messageElement);
    consoleLog.scrollTop = consoleLog.scrollHeight;
    let index = 0;
    const interval = setInterval(() => {
        messageElement.textContent += message.charAt(index);
        index++;
        if (index === message.length) {
            clearInterval(interval);
        }
    }, delay);
}

// Fonction pour mettre à jour la barre de progression
function updateProgress(percentage) {
    progressBar.style.width = `${percentage}%`;
    if (percentage >= 100) {
        setTimeout(() => {
            progressBar.style.width = '0%';
        }, 1000);
    }
}

// Fonction pour afficher une prévisualisation de l'image
function showImagePreview(imageUrl) {
    previewImage.src = imageUrl;
    previewImage.style.display = 'block';
}

// Fonction pour démarrer la webcam
function startWebcam() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            cameraContainer.style.display = 'block';
            typeConsoleMessage("Webcam démarrée avec succès.");
        })
        .catch((err) => {
            typeConsoleMessage("Erreur d'accès à la webcam: " + err);
        });
}

// Fonction pour envoyer l'image au backend
function uploadImage(imageData) {
    typeConsoleMessage("Envoi de l'image au serveur...");
    updateProgress(20);
    return fetch('/upload', {
        method: 'POST',
        body: imageData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            typeConsoleMessage("Erreur lors de l'envoi de l'image: " + data.error);
            updateProgress(0);
            return null;
        } else {
            typeConsoleMessage("Image envoyée avec succès.");
            typeConsoleMessage("Texte extrait : " + data.extracted_text);
            updateProgress(50);
            return data.extracted_text;
        }
    })
    .catch(error => {
        typeConsoleMessage("Erreur lors de l'envoi de l'image: " + error);
        updateProgress(0);
        return null;
    });
}

// Fonction pour rechercher sur eBay avec le texte extrait
function searchEbay(query) {
    typeConsoleMessage("Recherche sur eBay pour: " + query);
    updateProgress(70);
    fetch('/search_ebay', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            typeConsoleMessage("Erreur lors de la recherche eBay: " + data.error);
            updateProgress(0);
        } else {
            typeConsoleMessage("Résultats de recherche obtenus.");
            updateProgress(100);
            // Afficher les résultats sur la page
            resultsContainer.innerHTML = data.results.map(item => `
                <div class="result-item">
                    <img src="${item.image || 'https://via.placeholder.com/80'}" alt="Image non disponible">
                    <div>
                        <h3><a href="${item.url}" target="_blank">${item.title}</a></h3>
                        <p>Prix : ${item.price} USD</p>
                    </div>
                </div>
            `).join('');
        }
    })
    .catch(error => {
        typeConsoleMessage("Erreur lors de la recherche eBay: " + error);
        updateProgress(0);
    });
}

// Événements pour activer la webcam, téléverser une image et démarrer la recherche
startWebcamBtn.addEventListener('click', () => {
    startWebcam();
});

uploadBtn.addEventListener('click', () => {
    uploadInput.click();
});

uploadInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    typeConsoleMessage("Téléversement d'une image sélectionnée...");
    const formData = new FormData();
    formData.append('file', file);
    const imageUrl = URL.createObjectURL(file);
    showImagePreview(imageUrl);
    uploadImage(formData).then(extractedText => {
        if (extractedText) {
            searchEbay(extractedText);
        }
    });
});

// Action du bouton "Go"
goBtn.addEventListener('click', () => {
    typeConsoleMessage("Recherche lancée.");
    const formData = new FormData();
    uploadImage(formData).then(extractedText => {
        if (extractedText) {
            searchEbay(extractedText);
        }
    });
});

