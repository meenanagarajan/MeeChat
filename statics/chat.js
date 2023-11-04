document.addEventListener("DOMContentLoaded", function() {
    var chatLog = document.getElementById("chat-log");
    var userInput = document.getElementById("user-input");
    var sendButton = document.getElementById("send-button");

    sendButton.addEventListener("click", function() {
        var userMessage = userInput.value;
        if (userMessage) {
            addMessage("You: " + userMessage);
            userInput.value = "";

            // Send user message to the server
            sendUserMessage(userMessage);
        }
    });

    function addMessage(message) {
        var messageDiv = document.createElement("div");
        messageDiv.textContent = message;
        chatLog.appendChild(messageDiv);
    }

    function sendUserMessage(message) {
        // Send user message to the server and handle chatbot response
        fetch("/api/chat", {
            method: "POST",
            body: JSON.stringify({ message: message }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            addMessage("ChatGPT: " + data.response);
        })
        .catch(function(error) {
            console.error("Error:", error);
        });
    }
});
