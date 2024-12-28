const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const handleToggleInput = (e) => {
  if (showPasswordToggle.textContent === "Show") {
    // passwordField.type = "text";
    showPasswordToggle.textContent = "Hide";
    passwordField.setAttribute("type", "text");
  } else {
    // passwordField.type = "password";
    showPasswordToggle.textContent = "Show";
    passwordField.setAttribute("type", "password");
  }
};
showPasswordToggle.addEventListener("click", handleToggleInput);
