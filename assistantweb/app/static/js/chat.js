// app/static/js/chat.js
const socket = io();
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addSuggestions(suggestions) {
    const buttonsDiv = document.createElement('div');
    buttonsDiv.className = 'suggestion-buttons';
    
    suggestions.forEach(suggestion => {
        const button = document.createElement('button');
        button.className = 'btn btn-outline-primary btn-sm';
        button.textContent = suggestion.text;
        button.onclick = () => {
            socket.emit('message', { text: suggestion.value });
            addMessage(suggestion.text, true);
            buttonsDiv.remove();
        };
        buttonsDiv.appendChild(button);
    });
    
    chatMessages.appendChild(buttonsDiv);
}

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('message', { text: message });
        addMessage(message, true);
        messageInput.value = '';
    }
});

socket.on('response', (data) => {
    addMessage(data.text);
    if (data.suggestions) {
        addSuggestions(data.suggestions);
    }
});
