document.addEventListener("DOMContentLoaded", function() {

document.getElementById("loginForm").addEventListener("submit", function(event) {

  event.preventDefault();

  var employeeIDInput = document.getElementById("employeeIDInput");
  var passwordInput = document.getElementById("passwordInput");

  const employeeIDInputValue = employeeIDInput.value.trim();
  const passwordInputValue = passwordInput.value.trim();

  if (employeeIDInputValue === "") {
    employeeIDInput.classList.add("is-invalid");
  }
  if (passwordInputValue === "") {
    passwordInput.classList.add("is-invalid");
  }

  if (employeeIDInputValue === '' || passwordInputValue === '') {
       // pass
  } else {
      var loginButton = document.getElementById("login-button");
      loginButton.disabled = true;

      var spinner = document.createElement('div');
      spinner.className = " ms-2 spinner-border text-light spinner-border-sm";
      spinner.id = "verifySpinner";
      loginButton.appendChild(spinner);

      var formData = new FormData(this);

      // Perform AJAX request
      $.ajax({
       url: $(this).attr('action'),
       type: $(this).attr('method'),
       data: formData,
       processData: false,
       contentType: false,
       success: function(response) {
         var status = response["message"];

         if (status == "auth_error") {
           loginButton.disabled = false;
           verifySpinner.remove()
           passwordInput.classList.add("is-invalid");

         } else if (status == "success") {
            window.location.href = window.location.protocol + '//' + window.location.host;
         }

       },
       error: function(xhr, status, error) {
         loginButton.disabled = false;
         verifySpinner.remove()
      }
     });
  }

});

});