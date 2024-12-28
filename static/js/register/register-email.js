const emailField = document.querySelector("#emailField");
const emailfeedBackArea = document.querySelector(".emailfeedBackArea");
// email validation
emailField.addEventListener("keyup", (e) => {
  const emailValue = e.target.value;
  emailField.classList.remove("is-invalid");
  emailfeedBackArea.style.display = "none";
  if (emailValue.length > 0) {
    fetch("/auth/validate-email/", {
      body: JSON.stringify({ email: emailValue }),
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.email_error) {
          submitButton.disabled = true;
          emailField.classList.add("is-invalid");
          emailfeedBackArea.style.display = "block";
          emailfeedBackArea.style.color = "red";
          emailfeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          submitButton.removeAttribute("disabled");
        }
      });
  }
});
