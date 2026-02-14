document.addEventListener("DOMContentLoaded", function () {
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const toggleThemeBtn = document.getElementById("toggleTheme");

    // Initialize Theme
    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.classList.add(savedTheme + "-mode");
    updateThemeUI(savedTheme === "dark");

    if (sendButton) {
        sendButton.addEventListener("click", sendMessage);
    }

    if (userInput) {
        userInput.addEventListener("keydown", function (event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });
    }

    if (toggleThemeBtn) {
        toggleThemeBtn.addEventListener("click", toggleTheme);
    }
});

async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatBox = document.getElementById("chat-box");
    const message = userInput.value.trim();

    if (message === "" || sendButton.classList.contains("loading")) return;

    // UI State: Loading
    appendMessage("user", message);
    userInput.value = "";
    setLoading(true);

    try {
        const response = await fetch("/run_api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: message })
        });

        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }

        const data = await response.json();
        if (data.status === "success") {
            appendMessage("bot", data.result.message, true);
        } else {
            throw new Error(data.message || "Unknown error");
        }
    } catch (error) {
        console.error("Chat Error:", error);
        appendMessage("bot", "Sorry, I encountered an error connecting to the server. Please try again later.");
    } finally {
        setLoading(false);
    }
}

function appendMessage(sender, message, markdown = false) {
    const chatBox = document.getElementById("chat-box");
    let messageElement;

    if (markdown && sender === "bot") {
        messageElement = document.createElement("md-block");
        messageElement.textContent = message;
    } else {
        messageElement = document.createElement("div");
        messageElement.innerHTML = message.replace(/\n/g, "<br>");
    }

    messageElement.classList.add("chat-message", sender === "user" ? "user-message" : "bot-message");
    chatBox.appendChild(messageElement);
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: 'smooth'
    });
}

function setLoading(isLoading) {
    const sendButton = document.getElementById("send-button");
    const userInput = document.getElementById("user-input");

    if (isLoading) {
        sendButton.classList.add("loading");
        sendButton.disabled = true;
        userInput.disabled = true;
    } else {
        sendButton.classList.remove("loading");
        sendButton.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.classList.contains("dark-mode");
    const newTheme = isDark ? "light" : "dark";

    html.classList.remove("light-mode", "dark-mode");
    html.classList.add(newTheme + "-mode");
    localStorage.setItem("theme", newTheme);
    updateThemeUI(!isDark);
}

function updateThemeUI(isDark) {
    const button = document.getElementById("toggleTheme");
    const logo = document.querySelector(".logo");

    if (button) button.innerHTML = isDark ? "☀️" : "🌙";

    if (logo) {
        const lightLogo = logo.getAttribute("data-light");
        const darkLogo = logo.getAttribute("data-dark");
        logo.src = isDark ? darkLogo : lightLogo;
    }
}
