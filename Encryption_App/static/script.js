document.addEventListener("DOMContentLoaded", () => {
    const main = document.querySelector("main");

    document.addEventListener('mouseenter', () => {
        main.style.filter = `blur(0px)`;
    });

    document.addEventListener('mouseleave', () => {
        main.style.filter = `blur(30px)`;
    });

    const navToggle = document.getElementById("hideNav");
    const nav = document.querySelector("nav");
    const bottomButtons = document.querySelector(".buttons");
    const hiddenButtons = document.querySelector(".hiddenNavButtons");
    const fullButtons = document.querySelector(".fullNavButtons");
    const themeToggle = document.getElementById("themeToggle");

    // Check the cookie for the nav state
    const navState = getCookie("navState") || "shown";
    if (navState === "hidden") {
        nav.classList.add("hidden");
        navToggle.classList.add("hidden");
        bottomButtons.classList.add("hidden");
        hiddenButtons.classList.add("hidden");
        fullButtons.classList.add("hidden");
    }

    navToggle.addEventListener("click", () => {
        const isHidden = nav.classList.toggle("hidden");
        navToggle.classList.toggle("hidden");
        bottomButtons.classList.toggle("hidden");
        hiddenButtons.classList.toggle("hidden");
        fullButtons.classList.toggle("hidden");
        
        setCookie("navState", isHidden ? "hidden" : "shown", 30);
    });

    // Check the cookie for the theme state
    const currentTheme = getCookie("theme") || "light";
    if (currentTheme === "dark") {
        document.body.classList.add("dark-mode");
    }

    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        const newTheme = document.body.classList.contains("dark-mode") ? "dark" : "light";
        setCookie("theme", newTheme, 30);
    });

    function setCookie(name, value, days) {
        const d = new Date();
        d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + d.toUTCString();
        document.cookie = `${name}=${value};${expires};path=/`;
    }

    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

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