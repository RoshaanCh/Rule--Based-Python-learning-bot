/* ======================================
   My Python Buddy - Interactive JavaScript
   ====================================== */

// Configuration
const API_URL = 'https://my-python-buddy.vercel.app/';
const SUGGESTIONS_URL = 'https://my-python-buddy.vercel.app/';

// DOM Elements
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.querySelector('.send-btn');
const messagesWrapper = document.querySelector('.messages-wrapper');
const chatContainer = document.querySelector('.chat-container');
const loadingIndicator = document.getElementById('loadingIndicator');
const newChatBtn = document.querySelector('.new-chat-btn');
const topicLinks = document.querySelectorAll('.topic-link');
const suggestionBtns = document.querySelectorAll('.suggestion-btn');

// State
let isLoading = false;
let conversationHistory = [];

// ======================================
// Initialization
// ======================================

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    autoResizeTextarea();
    loadConversationHistory();
});

function setupEventListeners() {
    // Chat form submission
    chatForm.addEventListener('submit', handleSendMessage);

    // Textarea auto-resize and enter key handling
    messageInput.addEventListener('input', autoResizeTextarea);
    messageInput.addEventListener('keydown', handleKeyDown);

    // Topic links
    topicLinks.forEach(link => {
        link.addEventListener('click', handleTopicClick);
    });

    // Suggestion buttons
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', handleSuggestionClick);
    });

    // New chat button
    newChatBtn.addEventListener('click', startNewChat);
}

// ======================================
// Message Handling
// ======================================

function handleSendMessage(e) {
    e.preventDefault();

    const message = messageInput.value.trim();

    if (!message) return;

    // Validate message length
    if (message.length > 5000) {
        showNotification('Message is too long (max 5000 characters)', 'error');
        return;
    }

    // Add user message to UI
    addMessage(message, 'user');

    // Clear input
    messageInput.value = '';
    autoResizeTextarea();

    // Send to backend
    sendMessageToBackend(message);
}

function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
}

async function sendMessageToBackend(message) {
    if (isLoading) return;

    isLoading = true;
    sendBtn.disabled = true;
    showLoadingIndicator(true);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.status === 'success') {
            // Add bot response to UI
            addMessage(data.bot_response, 'bot');

            // Save to history
            conversationHistory.push({
                user: message,
                bot: data.bot_response,
                timestamp: new Date().toISOString()
            });
            saveConversationHistory();
        } else {
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage(
            'Connection error. Make sure the backend is running on http://127.0.0.1:5000',
            'bot'
        );
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        showLoadingIndicator(false);
        messageInput.focus();
    }
}

function addMessage(content, sender) {
    const messageGroup = document.createElement('div');
    messageGroup.className = `message-group ${sender}-group`;

    if (sender === 'bot') {
        // Add bot avatar
        const botAvatar = document.createElement('div');
        botAvatar.className = 'bot-avatar';
        botAvatar.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
            </svg>
        `;
        messageGroup.appendChild(botAvatar);
    }

    const message = document.createElement('div');
    message.className = `message ${sender}-message`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    // Parse content for markdown-like formatting
    messageContent.innerHTML = parseMessageContent(content);

    message.appendChild(messageContent);
    messageGroup.appendChild(message);

    messagesWrapper.appendChild(messageGroup);

    // Scroll to bottom
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 0);
}

function parseMessageContent(content) {
    let html = content;

    // Escape HTML
    const div = document.createElement('div');
    div.textContent = content;
    html = div.innerHTML;

    // Bold text
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Code snippets
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Line breaks
    html = html.replace(/\n/g, '<br>');

    // Links
    html = html.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );

    return html;
}

// ======================================
// UI Interactions
// ======================================

function handleTopicClick(e) {
    e.preventDefault();
    const question = e.target.dataset.question;
    if (question) {
        messageInput.value = question;
        messageInput.focus();
        autoResizeTextarea();
    }
}

function handleSuggestionClick(e) {
    const question = e.target.dataset.question;
    if (question) {
        messageInput.value = question;
        sendBtn.click();
    }
}

function startNewChat() {
    // Clear messages except welcome
    const welcomeGroup = document.querySelector('.welcome-group');
    messagesWrapper.innerHTML = '';
    messagesWrapper.appendChild(welcomeGroup);

    // Clear history
    conversationHistory = [];
    saveConversationHistory();

    // Reset input
    messageInput.value = '';
    autoResizeTextarea();
    messageInput.focus();

    // Scroll to top
    chatContainer.scrollTop = 0;
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    const scrollHeight = messageInput.scrollHeight;
    const maxHeight = 120; // 120px max

    if (scrollHeight > maxHeight) {
        messageInput.style.height = maxHeight + 'px';
    } else {
        messageInput.style.height = Math.max(scrollHeight, 40) + 'px';
    }
}

function showLoadingIndicator(show) {
    if (show) {
        loadingIndicator.classList.add('active');
    } else {
        loadingIndicator.classList.remove('active');
    }
}

function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Can be enhanced with a toast notification library
}

// ======================================
// Conversation History
// ======================================

function saveConversationHistory() {
    try {
        localStorage.setItem('pyBuddyHistory', JSON.stringify(conversationHistory));
    } catch (e) {
        console.warn('Could not save conversation history:', e);
    }
}

function loadConversationHistory() {
    try {
        const saved = localStorage.getItem('pyBuddyHistory');
        if (saved) {
            conversationHistory = JSON.parse(saved);
        }
    } catch (e) {
        console.warn('Could not load conversation history:', e);
        conversationHistory = [];
    }
}

// ======================================
// Utility Functions
// ======================================

function formatTime(timestamp) {
    return new Date(timestamp).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getGreeting() {
    const hour = new Date().getHours();
    if (hour < 12) return '🌅 Good morning!';
    if (hour < 18) return '☀️ Good afternoon!';
    return '🌙 Good evening!';
}

// ======================================
// Performance Optimizations
// ======================================

// Lazy load theme
function applyTheme() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (!isDark) {
        document.documentElement.style.colorScheme = 'dark';
    }
}

applyTheme();

// Listen for theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);

// ======================================
// Accessibility Features
// ======================================

// Announce loading to screen readers
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    document.body.appendChild(announcement);

    setTimeout(() => announcement.remove(), 1000);
}

// ======================================
// Error Handling & Validation
// ======================================

window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

// Connection test
async function testConnection() {
    try {
        const response = await fetch('http://127.0.0.1:5000/', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        return response.ok;
    } catch (e) {
        return false;
    }
}

// Initialize connection check on load
window.addEventListener('load', async () => {
    const connected = await testConnection();
    if (!connected) {
        console.warn('Backend server not available. Please start the Flask server.');
        showNotification(
            'Backend not available. Start the Flask server with: python app.py',
            'warning'
        );
    }
});

// ======================================
// Mobile-specific Features
// ======================================

if (/Mobile|Android|iPhone|iPad|iPod/.test(navigator.userAgent)) {
    // Disable zoom on input focus for mobile
    document.addEventListener('touchstart', function (e) {
        if (e.target === messageInput) {
            document.addEventListener('gesturestart', preventZoom, false);
        }
    });

    function preventZoom(e) {
        if (e.scale !== 1) {
            e.preventDefault();
        }
    }
}

// ======================================
// Development Helpers
// ======================================

// Add test data for development
window.addTestMessage = function(message, sender = 'bot') {
    addMessage(message, sender);
};

// Clear all data
window.clearAllData = function() {
    localStorage.clear();
    conversationHistory = [];
    startNewChat();
};

// Export console helpers
console.log('%cMy Python Buddy Commands:', 'color: #58a6ff; font-size: 14px; font-weight: bold;');
console.log('%cwindow.addTestMessage(text, sender)', 'color: #79c0ff;');
console.log('%cwindow.clearAllData()', 'color: #79c0ff;');
