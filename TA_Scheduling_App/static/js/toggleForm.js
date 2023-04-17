let buttonIds = ["create-button", "delete-button", "add-button","deleteTA-button"];

buttonIds.forEach(function(id) {
  let button = document.getElementById(id);
  button.addEventListener("click", toggleForm);
});

function toggleForm() {
  let formContainer = this.nextElementSibling;
  if (formContainer.style.display === "none") {
    formContainer.style.display = "block";
  } else {
    formContainer.style.display = "none";
  }
}

