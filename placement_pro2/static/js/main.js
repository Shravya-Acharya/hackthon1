// Chatbot functionality
function toggleChatbot() {
    document.getElementById('chatbotContainer').classList.toggle('active');
}

function sendMessage() {
    const input = document.getElementById('chatbotInput');
    const message = input.value.trim();
    if (!message) return;

    // Add user message
    const messages = document.getElementById('chatbotMessages');
    const userDiv = document.createElement('div');
    userDiv.className = 'message user-message';
    userDiv.textContent = message;
    messages.appendChild(userDiv);

    // Clear input
    input.value = '';

    // Send to server
    fetch('/chatbot', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        const botDiv = document.createElement('div');
        botDiv.className = 'message bot-message';
        botDiv.textContent = data.response;
        messages.appendChild(botDiv);
        messages.scrollTop = messages.scrollHeight;
    });
}

// Auto-hide alerts after 3 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 3000);
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required]');
    for (let input of inputs) {
        if (!input.value.trim()) {
            alert(`${input.name} is required`);
            input.focus();
            return false;
        }
    }
    return true;
}

// Confirm actions
function confirmAction(message, url) {
    if (confirm(message)) {
        window.location.href = url;
    }
}

// Dynamic search/filter
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let found = false;
        
        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell) {
                const textValue = cell.textContent || cell.innerText;
                if (textValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        rows[i].style.display = found ? '' : 'none';
    }
}