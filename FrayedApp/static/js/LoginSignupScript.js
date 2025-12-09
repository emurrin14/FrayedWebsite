document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("SignUpForm");
    const emailInput = document.querySelector(".SignUpEmailInput");
    const p1Input = document.querySelector(".SignUpPasswordInput");
    const p2Input = document.querySelector(".SignUpPassword2Input");
    const errorDiv = document.getElementById("errorDiv");

    form.addEventListener("submit", function (event) {
        errorDiv.style.display = "none";
        errorDiv.textContent = "";

        if (p1Input.value !== p2Input.value) {
          event.preventDefault();
          errorDiv.textContent = "Passwords do not match.";
          errorDiv.style.display = "block";
        }
    });
});