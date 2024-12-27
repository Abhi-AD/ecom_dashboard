const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
usernameField.addEventListener("keyup", (e) => {
  const usernameValue = e.target.value;

  usernameField.classList.remove("is-invalid");
  feedBackArea.style.display = "none";

  if (usernameValue.length > 0) {
    fetch("/auth/validate-username/", {
      body: JSON.stringify({ username: usernameValue }),
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Data", data);
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          feedBackArea.style.display = "block";
          feedBackArea.style.color = "red";
          feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
        }
      });
  }
});
