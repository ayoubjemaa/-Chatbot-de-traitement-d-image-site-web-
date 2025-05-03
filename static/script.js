// Sélection des éléments du DOM
const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const fileInputs = [document.querySelector("#file-input"), document.querySelector("#file-input1")];
const fileWrappers = [document.querySelector(".file-upload-wrapper"), document.querySelector(".file-upload-wrapper1")];
const fileCancelButtons = [document.querySelector("#file-cancel"), document.querySelector("#file-cancel1")];
const fileUploadButtons = [document.querySelector("#file-upload"), document.querySelector("#file-upload1")];

const userData = {
    message: null,
    files: [{ data: null, mime_type: null }, { data: null, mime_type: null }]
};

// Fonction pour afficher une alerte
const showAlert = (message) => {
    const alertContainer = document.getElementById("alert-container");
    alertContainer.querySelector(".alert-message").textContent = message;
    alertContainer.style.display = "block";
};

// Fonction pour fermer l'alerte
const closeAlert = () => document.getElementById("alert-container").style.display = "none";

// Fonction pour créer un élément de message
const createMessageElement = (content, ...classes) => {
    const div = document.createElement("div");
    div.classList.add("message", ...classes);
    div.innerHTML = content;
    return div;
};

// Générer la réponse du bot
const generateBotResponse = async (incomingMessageDiv) => {
    const messageElement = incomingMessageDiv.querySelector(".message-text");

    if (userData.files[0].data && userData.files[1].data) {
        try {
            const response = await fetch("http://127.0.0.1:5000/compare", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    image1: userData.files[0].data,
                    image2: userData.files[1].data,
                })
            });

            const result = await response.json();
            let botReply;
            if (result.same_person) {
                botReply = `✅ Same person detected. `; // Affiche le nom de l'image unique
            } else {
                botReply = `❌ Different people. `; // Affiche les noms des deux personnes
            }
            botReply += ` (Distance : ${result.distance.toFixed(4)})`;
            messageElement.innerHTML = botReply;
        } catch (error) {
            messageElement.innerHTML = "❌ Error while comparing.";
        }
    } else if (userData.files[0].data) {
        if (userMessage.includes("text") || userMessage.includes("text recognition")) {

                // Cas où une seule image est envoyée pour la reconnaissance de texte
                try {
                    const response = await fetch("http://127.0.0.1:5000/recognize_text", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            image1: userData.files[0].data
                        })
                    });
    
                    const result = await response.json();
                    let botReply = `📝 Texte détecté: ${result.recognized_text}`;
                    messageElement.innerHTML = botReply;
                } catch (error) {
                    messageElement.innerHTML = "❌ Error recognizing text.";
                }
            } else {
                messageElement.innerHTML = "❌ Aucun fichier image trouvé pour la reconnaissance du texte.";
            }
        // Cas où une seule image est envoyée pour reconnaissance d'objet
        try {
            const response = await fetch("http://127.0.0.1:5000/compare", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    image1: userData.files[0].data
                })
            });

            const result = await response.json();
            let botReply = `🔍 Object detected: ${result.object_name}`;
            messageElement.innerHTML = botReply;
        } catch (error) {
            messageElement.innerHTML = "❌ Error recognizing object.";
        }
    }
    else if (userData.files[0].data) {
        // Cas où une seule image est envoyée pour reconnaissance d'objet
        try {
            const response = await fetch("http://127.0.0.1:5000/compare", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    image1: userData.files[0].data
                })
            });

            const result = await response.json();
            let botReply = `🔍 Object detected: ${result.object_name}`;
            messageElement.innerHTML = botReply;
        } catch (error) {
            messageElement.innerHTML = "❌ Error recognizing object.";
        }
    } else {
        const userMessage = userData.message.toLowerCase();
        const greetings = ["hi", "hello", "hey", "good morning", "good evening"];
        const bye = ["stop", "bye", "good bye"];
        const thanksKeywords = ["merci", "thanks", "thank you", "merci beaucoup", "thanks a lot"];
        const okKeywords = ["ok", "d'accord", "c'est clair", "bien", "tout est bon", "ok d'accord"];

        let botReply = "I'm still learning! How can I assist you? 😊";

        if (greetings.some(greet => userMessage.includes(greet))) {
            botReply = "Hello! 🤖 I am your chatbot. How can I assist you today?";
        } else if (bye.some(byebye => userMessage.includes(byebye))) {
            botReply = "Good bye! See you later.";
            messageElement.style.color = "#ff0000";
        } else if (thanksKeywords.some(thank => userMessage.includes(thank))) {
            botReply = "You're welcome! 😊 Feel free to ask if you need help!";
        } else if (okKeywords.some(keyword => userMessage.includes(keyword))) {
            botReply = "Glad it's clear! 😊 Let me know if you need anything else!";
        }
        messageElement.innerHTML = botReply;
    }
    incomingMessageDiv.classList.remove("thinking");
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
    userData.files = [{}, {}];
};

// Gérer l'envoi des messages
const handleOutgoingMessage = (e) => {
    e.preventDefault();
    userData.message = messageInput.value.trim();

    if (!userData.message && !userData.files[0].data && !userData.files[1].data) return;

    messageInput.value = "";
    fileWrappers.forEach(wrapper => wrapper.classList.remove("file-uploaded"));

    const messageContent = `
        <div class="message-text">${userData.message}</div>
        ${userData.files.map(file => file.data ? `<img src="data:${file.mime_type};base64,${file.data}" class="attachment"/>` : "").join("")}
    `;

    const userMessageDiv = createMessageElement(messageContent, "user-message");
    chatBody.appendChild(userMessageDiv);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

    const botMessageDiv = createMessageElement(`
        <svg xmlns="http://www.w3.org/2000/svg" class="bot-avatar" width="50" height="50" viewBox="0 0 1024 1024">
            <path d="M738.3 287.6H285.7c-59 0-106.8 47.8-106.8 106.8v303.1c0 59 47.8 106.8 106.8 106.8h81.5v111.1c0 .7.8 1.1 1.4.7l166.9-110.6 41.8-.8h117.4l43.6-.4c59 0 106.8-47.8 106.8-106.8V394.5c0-59-47.8-106.9-106.8-106.9zM351.7 448.2c0-29.5 23.9-53.5 53.5-53.5s53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5-53.5-23.9-53.5-53.5zm157.9 267.1c-67.8 0-123.8-47.5-132.3-109h264.6c-8.6 61.5-64.5 109-132.3 109zm110-213.7c-29.5 0-53.5-23.9-53.5-53.5s23.9-53.5 53.5-53.5 53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5z"></path>
        </svg>
        <div class="message-text">
            <div class="thinking-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>`, "bot-message", "thinking"
    );

    chatBody.appendChild(botMessageDiv);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

    setTimeout(() => generateBotResponse(botMessageDiv), 600);
};

// Ajout des événements
messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleOutgoingMessage(e);
});
sendMessageButton.addEventListener("click", handleOutgoingMessage);

// Gestion des fichiers
fileInputs.forEach((input, index) => {
    input.addEventListener("change", () => {
        const file = input.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            fileWrappers[index].querySelector("img").src = e.target.result;
            fileWrappers[index].classList.add("file-uploaded");
            userData.files[index] = { data: e.target.result.split(",")[1], mime_type: file.type };
            input.value = "";
        };
        reader.readAsDataURL(file);
    });
});

// Annuler l'upload
fileCancelButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        userData.files[index] = {};
        fileWrappers[index].classList.remove("file-uploaded");
    });
});

// Déclencher le sélecteur de fichier
fileUploadButtons.forEach((button, index) => {
    button.addEventListener("click", () => fileInputs[index].click());
});
