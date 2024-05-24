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
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.parentNode.removeChild(alert);
        });
    });
});

function parseURLParams(url) {
    var queryStart = url.indexOf("?") + 1,
        queryEnd   = url.indexOf("#") + 1 || url.length + 1,
        query      = url.slice(queryStart, queryEnd - 1),
        pairs      = query.replace(/\+/g, " ").split("&"),
        params     = {},
        i, keyValue, key, value;

    if (query === url || query === "") return params;

    for (i = 0; i < pairs.length; i++) {
        keyValue = pairs[i].split("=");
        key = decodeURIComponent(keyValue[0]);
        value = decodeURIComponent(keyValue[1] || "");
        params[key] = value;
    }
    return params;
}

function setActiveForm() {
    var params = parseURLParams(window.location.href);
    var signupForm = document.getElementById('signupForm');
    var loginForm = document.getElementById('loginForm');
    var toggleLink = document.getElementById('toggleLink');

    if (params["signup"] === "1") {
        loginForm.classList.remove("active");
        signupForm.classList.add("active");
        toggleLink.innerHTML = "Already have an account? <a href='#'>Login!</a>";
    }
}

// Call the setActiveForm function when the page loads
window.onload = setActiveForm;