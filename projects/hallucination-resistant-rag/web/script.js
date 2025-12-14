document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');
    const sendBtn = document.getElementById('send-btn');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = userInput.value.trim();
        if (!question) return;

        // Add user message
        addMessage(question, 'user');
        userInput.value = '';
        sendBtn.disabled = true;

        // Add loading indicator
        const loadingId = addLoadingMessage();

        try {
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            
            // Remove loading and add bot response
            removeMessage(loadingId);
            addMessage(formatBotResponse(data.response), 'bot', true);

        } catch (error) {
            removeMessage(loadingId);
            addMessage("Sorry, something went wrong. Please ensure the backend is running.", 'bot');
            console.error('Error:', error);
        } finally {
            sendBtn.disabled = false;
            userInput.focus();
        }
    });

    function addMessage(text, sender, isHTML = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        
        if (isHTML) {
            contentDiv.innerHTML = text;
        } else {
            contentDiv.textContent = text;
        }

        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv.id = 'msg-' + Date.now();
    }

    function addLoadingMessage() {
        const id = 'loading-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot-message');
        messageDiv.id = id;
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.innerHTML = '<span class="typing-dot">.</span><span class="typing-dot">.</span><span class="typing-dot">.</span>';
        
        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function formatBotResponse(text) {
        // Simple formatter to convert --- Source --- blocks into styled HTML
        // This regex looks for patterns like "--- Source 1 ---"
        
        // Escape HTML first to prevent XSS (basic)
        let safeText = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

        // Restore newlines
        safeText = safeText.replace(/\n/g, '<br>');

        // Highlight "Answer based on..."
        if (safeText.includes('Answer based on retrieved context:')) {
            safeText = safeText.replace('Answer based on retrieved context:', '<strong>Answer based on retrieved context:</strong>');
        }

        // Improved output handling for the specific separation format we implemented in generate.py
        // We look for the separator line to style the output better
        safeText = safeText.replace(/### Retrieved Information:/g, '<div style="margin-bottom:10px; font-weight:600; color:#a78bfa;">Retrieved Evidence:</div>');
        
        // Style source blocks
        safeText = safeText.replace(/--- Source (\d+) ---<br>(.*?)<br><br>/g, 
            '<div class="source-block"><div class="source-header">Source $1</div>$2</div>');
        
        // Handle "System Note"
        safeText = safeText.replace(/System Note:/g, '<br><em>System Note:');

        return safeText;
    }
});
