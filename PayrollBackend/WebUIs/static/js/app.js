document.addEventListener("DOMContentLoaded", function() {


document.getElementById("searchForm").addEventListener("submit", function(event) {

  event.preventDefault();
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
        var employee_id = response['employee_id']; // Declare the employee_id variable
        console.log(employee_id); // Log the employee_id value to the console

        if (status == "error") {
            // handle error here
        } else if (status == "success") {

            var employeeLink = document.getElementById('employee_link');
            employeeLink.textContent = response.employee_id;
            employeeLink.href = '/employee/' + response.employee_id;

            // Format the other details and set them in the employee_details element
            var employeeDetails = document.getElementById('employee_details');
            var formattedDetails = response.first_name + ' ' + response.last_name + ', ' +
                'Email: ' + response.email + ', ' +
                'Phone: ' + response.phone;
            employeeDetails.textContent = formattedDetails;
        }
    },
    error: function(xhr, status, error) {
        // handle another error here
    }
})
});

});