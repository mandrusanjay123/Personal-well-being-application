// schedule.js handles AJAX requests for editing tasks

function editTask(taskId) {
    const newTimeSlot = prompt("Enter new time slot:");
    if (newTimeSlot) {
        fetch('/update_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ taskId: taskId, newTimeSlot: newTimeSlot })
        })
        .then(response => response.json())
        .then(data => alert(data.status))
        .catch(error => console.error('Error:', error));
    }
}
