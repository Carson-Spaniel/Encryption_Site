document.addEventListener("DOMContentLoaded", () => {
    // Function to clear all input fields
    function clearAllInputs() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        const passwordInput = document.getElementById('password');

        // Clear file inputs
        fileInputs.forEach(input => {
            input.value = ''; // Clear the value
            const fileNameDiv = document.getElementById(input.id + 'Name');
            if (fileNameDiv) {
                fileNameDiv.textContent = ''; // Clear displayed file name
            }
        });

        // Clear password input
        if (passwordInput) {
            passwordInput.value = '';
        }
    }

    // Call the function to clear inputs when the page loads
    clearAllInputs();
});

// Function to handle drag over the drop box
function handleDragOver(event) {
    event.preventDefault();
}

// Function to handle drag enter the drop box
function handleDragEnter(event, id) {
    document.getElementById(id).classList.add('highlight');
}

// Function to handle drag leave the drop box
function handleDragLeave(event, id) {
    document.getElementById(id).classList.remove('highlight');
}

// Function to handle drop files onto the drop box
function handleDrop(event, id) {
    event.preventDefault();
    document.getElementById(id).classList.remove('highlight');

    const files = event.dataTransfer.files;
    handleFiles(files, id);
}

// Function to handle files selected from input and display file name
function displayFileName(inputId) {
    const input = document.getElementById(inputId);
    const fileName = document.getElementById(inputId + 'Name');

    if (input.files.length > 0) {
        fileName.textContent = 'Selected File: ' + input.files[0].name;
    } else {
        fileName.textContent = '';
    }
}

// Function to handle files selected from input
function handleFiles(files, id) {
    if (files.length > 0) {
        const inputField = document.getElementById(id);
        inputField.files = files;
        displayFileName(id);
    }
}

function hideEmbed(button){
    const embed = document.querySelector('embed');
    if(embed){
        embed.parentNode.removeChild(embed);
    }

    const download = document.querySelector('.download');
    if(download){
        download.parentNode.removeChild(download);
    }

    const responseMessage = document.querySelector('#responseMessage');
    responseMessage.classList = "";
    responseMessage.textContent = "";

    const fileName = document.getElementById("file1" + 'Name');
    fileName.textContent = "";
}

function resetForm(){
    const fileName = document.getElementById("file1" + 'Name');
    fileName.textContent = "";
}

function matchPassword() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const matchMessage = document.getElementById('match');

    if (password !== confirmPassword) {
        matchMessage.innerText = "Passwords do not match.";
        matchMessage.classList = "not-match";
    } else {
        matchMessage.innerText = "";
        matchMessage.classList = "";
    }
}

function checkPasswordStrength(password) {
    const meter = document.getElementById('password-strength-meter');
    const text = document.getElementById('password-strength-text');

    const strength = {
        0: "Worst",
        1: "Bad",
        2: "Weak",
        3: "Good",
        4: "Strong",
        5: "Strong"
    };

    let score = 0;
    if (password.length >= 8) {
        score++;
    }
    if (password.length >= 16) {
        score++;
    }
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) {
        score++;
    }
    if (password.match(/[0-9]/)) {
        score++;
    }
    if (password.match(/[$@#&!]/)) {
        score++;
    }

    meter.value = score;
    text.innerHTML = strength[score];
}

// Helper function to get filename from headers
function getFilenameFromHeaders(headers) {
    const contentDisposition = headers.get('content-disposition');
    if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="([^"]+)"/);
        if (filenameMatch && filenameMatch.length > 1) {
            return filenameMatch[1];
        }
    }
    return 'file'; // Default filename
}