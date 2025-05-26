document.addEventListener("DOMContentLoaded", function() {
    var userInput = document.getElementById("user-input");
    var sendButton = document.getElementById("send-button");

    if (sendButton) {
        sendButton.addEventListener("click", sendMessage);
    } else {
        console.error("send-button not found in the document.");
    }

    if (userInput) {
        userInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });
    } else {
        console.error("user-input not found in the document.");
    }
});

function sendMessage() {
    var userInput = document.getElementById("user-input");
    var chatBox = document.getElementById("chat-box");
    var message = userInput.value.trim();

    if (message === "") return;

    appendMessage("user", message);
    userInput.value = "";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5001/run_api", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            appendMessage("bot", data.result.message, true); // Set markdown = true for bot responses
        } else if (xhr.readyState === 4) {
            appendMessage("bot", "Error connecting to chatbot server.");
        }
    };
    
    xhr.send(JSON.stringify({ query: message }));
}

function appendMessage(sender, message, markdown = false) {
    var chatBox = document.getElementById("chat-box");
    var messageElement;

    if (markdown && sender === "bot") {
        messageElement = document.createElement("md-block");
        messageElement.innerText = message; // md-block automatically renders Markdown
    } else {
        messageElement = document.createElement("div");
        messageElement.innerHTML = message.replace(/\n/g, "<br>");
    }
    
    messageElement.classList.add("chat-message", sender === "user" ? "user-message" : "bot-message");
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function darkThemeFunction() {
    var element = document.body;
    element.classList.toggle("dark-mode");

    var button = document.getElementById("toggleTheme");
    var logo = document.querySelector(".logo");

    // Get light and dark logo paths from the data attributes
    var lightLogo = logo.getAttribute("data-light");
    var darkLogo = logo.getAttribute("data-dark");

    if (element.classList.contains("dark-mode")) {
        button.innerHTML = "☀️"; // Change to sun icon
        logo.src = darkLogo; // Switch to dark mode logo
    } else {
        button.innerHTML = "🌙"; // Change to moon icon
        logo.src = lightLogo; // Switch to light mode logo
    }
}
