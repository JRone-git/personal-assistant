// app/static/js/main.js
function toggleTask(taskId) {
    fetch(`/api/tasks/${taskId}/toggle`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    }).then(data => {
        if (data.status === 'success') {
            // Update UI
        }
    }).catch(error => console.error('Error:', error));
}

document.getElementById('task-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    fetch('/api/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(Object.fromEntries(formData))
    }).then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    }).then(data => {
        if (data.status === 'success') {
            location.reload();
        }
    }).catch(error => console.error('Error:', error));
});