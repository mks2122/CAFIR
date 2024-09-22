 
const signupForm = document.getElementById('login-form');

signupForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission

    // Validate form inputs
    const username = document.getElementById('name').value;
    const password = document.getElementById('password').value;

    // Check for empty fields
    if (!username ||  !password) {
        alert('Please fill in all required fields.');
        return;
    }

    // If all validation passes, submit the form or perform other actions

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });
    console.log('Form submitted successfully!');
    // Add your form submission logic here (e.g., sending data to a server)
});