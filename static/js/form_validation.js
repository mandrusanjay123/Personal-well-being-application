// Simple form validation before submitting task details
function validateForm() {
    const estimatedTime = document.forms["taskForm"]["estimated_time"].value;
    const stressLevel = document.forms["taskForm"]["stress_level"].value;

    if (estimatedTime < 1 || estimatedTime > 24) {
        alert("Estimated time must be between 1 and 24 hours.");
        return false;
    }
    if (stressLevel < 1 || stressLevel > 5) {
        alert("Stress level must be between 1 and 5.");
        return false;
    }
    return true;
}
