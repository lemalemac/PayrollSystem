document.addEventListener("DOMContentLoaded", function() {

document.getElementById("modifyForm").addEventListener("submit", function(event) {

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

         if (status == "error") {
           // handle error here

         } else if (status == "success") {
          // handle success here
         }

       },
       error: function(xhr, status, error) {
           // handle another error here
      }
     });
});

});