document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');
    const sendBtn = document.getElementById('send-btn');
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadStatus = document.getElementById('upload-status');
    const newSessionBtn = document.getElementById('new-session-btn');
    const filesList = document.getElementById('files-list');
    const filesContainer = document.getElementById('files-container');

    let currentSessionId = null;
    let uploadedFiles = [];

    function updateFilesList() {
        if (uploadedFiles.length === 0) {
            filesList.style.display = 'none';
            return;
        }
        
        filesContainer.innerHTML = '';
        uploadedFiles.forEach(fileName => {
            const li = document.createElement('li');
            li.textContent = '📄 ' + fileName;
            li.style.padding = '8px 12px';
            li.style.background = 'rgba(167, 139, 250, 0.1)';
            li.style.borderRadius = '8px';
            li.style.marginBottom = '8px';
            li.style.borderLeft = '3px solid #a78bfa';
            li.style.listStyle = 'none';
            filesContainer.appendChild(li);
        });
        
        filesList.style.display = 'block';
    }

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const file = fileInput.files[0];
        if (!file) {
            uploadStatus.textContent = 'Please select a file.';
            return;
        }

        uploadBtn.disabled = true;
        const uploadingMsg = currentSessionId ? 
            `Adding ${file.name} to session...` : 
            `Uploading and processing ${file.name}...`;
        uploadStatus.textContent = uploadingMsg;

        const formData = new FormData();
        formData.append('file', file);
        
        // Add session_id if exists
        let url = 'http://localhost:8000/api/upload';
        if (currentSessionId) {
            url += `?session_id=${currentSessionId}`;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const data = await response.json();
            currentSessionId = data.session_id;
            uploadedFiles = data.files_in_session || [data.file_name];
            
            updateFilesList();
            uploadStatus.textContent = `Successfully added ${file.name}!`;
            fileInput.value = ''; // Clear file input
            chatForm.style.display = 'flex'; // Show chat form
            newSessionBtn.style.display = 'inline-block'; // Show new session button
        } catch (error) {
            uploadStatus.textContent = `Error: ${error.message}`;
            console.error('Upload Error:', error);
        } finally {
            uploadBtn.disabled = false;
        }
    });

    newSessionBtn.addEventListener('click', () => {
        if (confirm('Start a new session? This will clear current uploads and chat history.')) {
            currentSessionId = null;
            uploadedFiles = [];
            filesList.style.display = 'none';
            newSessionBtn.style.display = 'none';
            chatForm.style.display = 'none';
            uploadStatus.textContent = 'Upload a PDF to begin chatting.';
            
            // Clear chat history except welcome message
            while (chatContainer.children.length > 1) {
                chatContainer.removeChild(chatContainer.lastChild);
            }
        }
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = userInput.value.trim();
        if (!question || !currentSessionId) return;

        addMessage(question, 'user');
        userInput.value = '';
        sendBtn.disabled = true;

        const loadingId = addLoadingMessage();

        try {
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question, session_id: currentSessionId }),
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            
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
        messageDiv.id = 'msg-' + Date.now();
        return messageDiv.id;
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
        let safeText = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        safeText = safeText.replace(/\n/g, '<br>');
        if (safeText.includes('Answer based on retrieved context:')) {
            safeText = safeText.replace('Answer based on retrieved context:', '<strong style="color:#a78bfa;">Answer based on retrieved context:</strong>');
        }
        if (safeText.includes('REFUSAL:')) {
            safeText = safeText.replace('REFUSAL:', '<strong style="color:#f87171;">⚠️ Cannot Answer:</strong>');
        }
        safeText = safeText.replace(/### Retrieved Information:/g, '<div style="margin-bottom:10px; font-weight:600; color:#a78bfa;">📚 Retrieved Evidence:</div>');
        safeText = safeText.replace(/--- Source (\d+) ---<br>(.*?)<br><br>/g, 
            '<div class="source-block"><div class="source-header">Source $1</div>$2</div>');
        safeText = safeText.replace(/System Note:/g, '<br><em style="color:#9ca3af;">System Note:');
        return safeText;
    }
});