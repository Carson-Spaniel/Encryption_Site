document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");
    const toggleLink = document.getElementById("toggleLink");

    toggleLink.addEventListener("click", function(event) {
        event.preventDefault();
        if (loginForm.classList.contains("active")) {
            loginForm.classList.remove("active");
            signupForm.classList.add("active");
            toggleLink.innerHTML = "Already have an account? <a href='#'>Login!</a>";
        } else {
            loginForm.classList.add("active");
            signupForm.classList.remove("active");
            toggleLink.innerHTML = "Don't have an account? <a href='#'>Sign up!</a>";
        }
    });
});
