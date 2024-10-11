document.getElementById('run').addEventListener('click', function () {
    const code = document.getElementById('code').value;
    const input = document.getElementById('input').value;
    const language = document.getElementById('language').value;

    // Prepare the request payload
    const data = {
        code: code,
        input: input,
        language: language
    };

    // Make AJAX request to backend with the correct URL
    fetch('/home/run_code/', {  // Updated URL to match /home/run_code/
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),  // Include CSRF token for Django
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        // Display the output or errors
        document.getElementById('output').textContent = data.output;
        document.getElementById('error').textContent = data.error;
    })
    .catch(error => {
        document.getElementById('error').textContent = 'Error: ' + error;
    });
});

// Helper function to get CSRF token
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
