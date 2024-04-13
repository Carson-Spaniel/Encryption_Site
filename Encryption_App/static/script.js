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